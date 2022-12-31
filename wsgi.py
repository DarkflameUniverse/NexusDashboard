from sys import platform
from app import create_app

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Extend the Flask shell context."""
    return {'app': app}

running_directly = __name__ == "wsgi" or __name__ == "__main__"
running_under_gunicorn = not running_directly and 'gunicorn' in __name__ and 'linux' in platform

# Configure development running
if running_directly:
    with app.app_context():
        app.run(host='0.0.0.0')

# Configure production running
if running_under_gunicorn:
    import logging
    from logging.handlers import RotatingFileHandler
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    file_handler = RotatingFileHandler('logs/nexus_dashboard.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(gunicorn_logger.level)

# Error out if nothing has been setup
if not running_directly and not running_under_gunicorn:
    raise RuntimeError('Unsupported WSGI server')
