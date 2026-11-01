"""Helpers for serving model / brick database files with validators and gzip.

Responses carry a strong ETag (derived from the source file's mtime and size,
or from a content hash for in-memory data) plus Last-Modified where available,
and honour conditional requests so repeat visits get cheap 304 responses.

When the client accepts gzip and ``COMPRESS_MODEL_RESPONSES`` is enabled the
body is gzip encoded. With ``CACHE_COMPRESSED_MODELS`` enabled a ``.gz``
copy is
stored on disk (regenerated whenever the source is newer) so no CPU is spent
per request; otherwise the body is compressed in memory at a fast level.
"""
import gzip
import hashlib
import mimetypes
import os
import pathlib
import tempfile
from datetime import datetime, timezone

from flask import Response, current_app, g, request, send_file
from flask.sessions import SecureCookieSessionInterface


# Fast level for on-the-fly compression, better level for stored copies
# (stored copies are only written once).
ON_THE_FLY_LEVEL = 1
STORED_LEVEL = 6


def _compression_enabled():
    return bool(current_app.config.get("COMPRESS_MODEL_RESPONSES", True))


def _store_compressed():
    return bool(current_app.config.get("CACHE_COMPRESSED_MODELS", False))


def _client_accepts_gzip():
    return _compression_enabled() and request.accept_encodings["gzip"] > 0


def _gz_path_for(path):
    """Location of the stored gzip copy for ``path``.

    Files inside the cache directory get a sibling ``.gz``; files that live
    elsewhere (e.g. the client's res/ folder, which may be read-only or shared)
    get a copy under ``<CACHE_LOCATION>/compressed/``.
    """
    cache_root = pathlib.Path(current_app.config["CACHE_LOCATION"]).resolve()
    path = path.resolve()
    try:
        path.relative_to(cache_root)
        return path.with_name(path.name + ".gz")
    except ValueError:
        digest = hashlib.sha1(str(path).encode()).hexdigest()
        return cache_root / "compressed" / f"{digest}-{path.name}.gz"


def _ensure_gz(path, src_stat):
    """Create/refresh the stored gzip copy of ``path`` and return its path."""
    gz_path = _gz_path_for(path)
    try:
        if gz_path.stat().st_mtime_ns >= src_stat.st_mtime_ns:
            return gz_path
    except FileNotFoundError:
        pass
    gz_path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "rb") as src:
        data = gzip.compress(src.read(), compresslevel=STORED_LEVEL, mtime=0)
    # write atomically so concurrent workers never serve a partial file
    fd, tmp = tempfile.mkstemp(
        dir=gz_path.parent, prefix=".tmp-", suffix=".gz"
    )
    try:
        with os.fdopen(fd, "wb") as out:
            out.write(data)
        os.chmod(tmp, 0o644)  # mkstemp creates 0600, match other cache files
        os.replace(tmp, gz_path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    return gz_path


def _skip_session_cookie():
    g.compressed_files_user_independent = True


class _SessionInterface(SecureCookieSessionInterface):
    """Skip refreshing the session cookie for user independent files.

    Flask-User refreshes the session cookie on every request, and Flask adds
    "Vary: Cookie" whenever it sets the cookie. As the cookie value changes on
    every response, the browser then has to revalidate every cached copy,
    defeating max-age. These files don't depend on the session, so there is
    nothing to save for them.
    """

    def save_session(self, app, session, response):
        if g.get("compressed_files_user_independent"):
            return None
        return super().save_session(app, session, response)


def register_compressed_files(app):
    if type(app.session_interface) is SecureCookieSessionInterface:
        app.session_interface = _SessionInterface()


def _finish(response, etag, last_modified, cache_control, vary):
    response.set_etag(etag)
    if last_modified is not None:
        response.last_modified = last_modified
    response.headers["Cache-Control"] = cache_control
    if vary:
        response.vary.add("Accept-Encoding")
    return response.make_conditional(request)


def _not_modified(etag, last_modified, cache_control, vary, mimetype):
    """Answer a matching conditional request without reading/compressing."""
    if etag in request.if_none_match:
        return _finish(
            Response(status=304, mimetype=mimetype),
            etag, last_modified, cache_control, vary
        )
    return None


def serve_file(path, mimetype, cache_control, user_independent=False):
    """Serve a file from disk with validators and optional gzip encoding.

    ``user_independent`` marks content that does not depend on the logged in
    user; the session cookie is not refreshed on these responses so no
    ``Vary: Cookie`` is added (see ``_SessionInterface``).
    """
    if user_independent:
        _skip_session_cookie()
    # absolute: send_file resolves relative paths against the app package
    path = pathlib.Path(path).resolve()
    if mimetype is None:
        mimetype = (
            mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        )
    st = path.stat()
    base_etag = f"{st.st_mtime_ns:x}-{st.st_size:x}"
    last_modified = datetime.fromtimestamp(int(st.st_mtime), tz=timezone.utc)
    vary = _compression_enabled()

    if not _client_accepts_gzip():
        response = send_file(
            path, mimetype=mimetype, etag=base_etag,
            last_modified=last_modified, conditional=True
        )
        response.headers["Cache-Control"] = cache_control
        if vary:
            response.vary.add("Accept-Encoding")
        return response

    etag = base_etag + "-gz"
    early = _not_modified(etag, last_modified, cache_control, vary, mimetype)
    if early is not None:
        return early

    if _store_compressed():
        gz_path = _ensure_gz(path, st)
        response = send_file(
            gz_path, mimetype=mimetype, etag=etag,
            last_modified=last_modified, conditional=True
        )
        response.headers["Cache-Control"] = cache_control
        response.headers["Content-Encoding"] = "gzip"
        response.vary.add("Accept-Encoding")
        return response

    with open(path, "rb") as src:
        data = gzip.compress(
            src.read(), compresslevel=ON_THE_FLY_LEVEL, mtime=0
        )
    response = Response(data, mimetype=mimetype)
    response.headers["Content-Encoding"] = "gzip"
    return _finish(response, etag, last_modified, cache_control, vary)


def serve_bytes(data, mimetype, cache_control, etag_seed=None):
    """Serve in-memory data (e.g. UGC lxfml from the database).

    ``etag_seed`` should be cheap, stable bytes identifying the content (for
    example the stored compressed blob); defaults to ``data``. ``data`` may
    be a callable producing the body, so a 304 can skip building it (this
    requires ``etag_seed``).
    """
    if callable(data):
        if etag_seed is None:
            data = data()
    if isinstance(data, str):
        data = data.encode()
    base_etag = hashlib.sha1(
        etag_seed if etag_seed is not None else data
    ).hexdigest()
    vary = _compression_enabled()
    gz = _client_accepts_gzip()
    etag = base_etag + ("-gz" if gz else "")

    early = _not_modified(etag, None, cache_control, vary, mimetype)
    if early is not None:
        return early

    if callable(data):
        data = data()
    if isinstance(data, str):
        data = data.encode()
    if gz:
        data = gzip.compress(data, compresslevel=ON_THE_FLY_LEVEL, mtime=0)
    response = Response(data, mimetype=mimetype)
    if gz:
        response.headers["Content-Encoding"] = "gzip"
    return _finish(response, etag, None, cache_control, vary)
