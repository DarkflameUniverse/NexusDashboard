import os
from flask import Flask, url_for, g, redirect
from functools import wraps
from flask_assets import Environment
from webassets import Bundle
import time
from app.models import db, migrate, PlayKey
from app.forms import CustomUserManager
from flask_user import user_registered, current_user, user_logged_in
from flask_wtf.csrf import CSRFProtect
from flask_apscheduler import APScheduler
from app.luclient import register_luclient_jinja_helpers
import pathlib

from app.commands import (
    init_db,
    init_accounts,
    load_property,
    gen_image_cache,
    gen_model_cache,
    fix_clone_ids,
    remove_buffs
)
from app.models import Account, AccountInvitation, AuditLog

import logging
from logging.handlers import RotatingFileHandler

from werkzeug.exceptions import HTTPException

# Instantiate Flask extensions
csrf_protect = CSRFProtect()
scheduler = APScheduler()
# db and migrate is instantiated in models.py


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # decrement uses on a play key after a successful registration
    # and increment the times it has been used
    @user_registered.connect_via(app)
    def after_register_hook(sender, user, **extra):
        if app.config["REQUIRE_PLAY_KEY"]:
            play_key_used = PlayKey.query.filter(PlayKey.id == user.play_key_id).first()
            play_key_used.key_uses = play_key_used.key_uses - 1
            play_key_used.times_used = play_key_used.times_used + 1
            app.logger.info(
                f"USERS::REGISTRATION User with ID {user.id} and name {user.username} Registered \
                using Play Key ID {play_key_used.id} : {play_key_used.key_string}"
            )
            db.session.add(play_key_used)
            db.session.commit()
        else:
            app.logger.info(f"USERS::REGISTRATION User with ID {user.id} and name {user.username} Registered")

    @user_logged_in.connect_via(app)
    def _after_login_hook(sender, user, **extra):
        app.logger.info(f"{user.username} Logged in")

    # A bunch of jinja filters to make things easiers
    @app.template_filter('ctime')
    def timectime(s):
        if s:
            return time.ctime(s)  # or datetime.datetime.fromtimestamp(s)
        else:
            return "Never"

    @app.template_filter('check_perm_map')
    def check_perm_map(perm_map, bit):
        if perm_map:
            return perm_map & (1 << bit)
        else:
            return 0 & (1 << bit)

    @app.template_filter('debug')
    def debug(text):
        print(text)

    @app.teardown_appcontext
    def close_connection(exception):
        cdclient = getattr(g, '_cdclient', None)
        if cdclient is not None:
            cdclient.close()

    @app.template_filter()
    def numberFormat(value):
        return format(int(value), ',d')


    # add the commands to flask cli
    app.cli.add_command(init_db)
    app.cli.add_command(init_accounts)
    app.cli.add_command(load_property)
    app.cli.add_command(gen_image_cache)
    app.cli.add_command(gen_model_cache)
    app.cli.add_command(fix_clone_ids)
    app.cli.add_command(remove_buffs)

    register_logging(app)
    register_settings(app)
    register_extensions(app)
    register_blueprints(app)
    register_luclient_jinja_helpers(app)

    # Extract the brickdb if it's not already extracted
    materials = pathlib.Path(f'{app.config["CACHE_LOCATION"]}Materials.xml')
    if not materials.is_file():
        # unzip the brickdb, and remove the import after
        from zipfile import ZipFile
        with ZipFile(f"{app.config['CLIENT_LOCATION']}res/brickdb.zip","r") as zip_ref:
            zip_ref.extractall(app.config["CACHE_LOCATION"])
        del ZipFile
        # copy over the brick primitives, and remove the import after
        from shutil import copytree
        copytree(f"{app.config['CLIENT_LOCATION']}res/brickprimitives", f"{app.config['CACHE_LOCATION']}brickprimitives")
        del copytree

    return app


def register_extensions(app):
    """Register extensions for Flask app

    Args:
        app (Flask): Flask app to register for
    """
    db.init_app(app)
    migrate.init_app(app, db)
    scheduler.init_app(app)
    scheduler.start()

    csrf_protect.init_app(app)

    user_manager = CustomUserManager(
        app, db, Account, UserInvitationClass=AccountInvitation
    )

    assets = Environment(app)
    assets.url = app.static_url_path
    scss = Bundle('scss/site.scss', filters='libsass', output='css/site.css')
    assets.register('scss_all', scss)


def register_blueprints(app):
    """Register blueprints for Flask app

    Args:
        app (Flask): Flask app to register for
    """

    from .main import main_blueprint
    app.register_blueprint(main_blueprint)
    from .play_keys import play_keys_blueprint
    app.register_blueprint(play_keys_blueprint, url_prefix='/play_keys')
    from .accounts import accounts_blueprint
    app.register_blueprint(accounts_blueprint, url_prefix='/accounts')
    from .characters import character_blueprint
    app.register_blueprint(character_blueprint, url_prefix='/characters')
    from .properties import property_blueprint
    app.register_blueprint(property_blueprint, url_prefix='/properties')
    from .moderation import moderation_blueprint
    app.register_blueprint(moderation_blueprint, url_prefix='/moderation')
    from .log import log_blueprint
    app.register_blueprint(log_blueprint, url_prefix='/log')
    from .bug_reports import bug_report_blueprint
    app.register_blueprint(bug_report_blueprint, url_prefix='/bug_reports')
    from .mail import mail_blueprint
    app.register_blueprint(mail_blueprint, url_prefix='/mail')
    from .luclient import luclient_blueprint
    app.register_blueprint(luclient_blueprint, url_prefix='/luclient')
    from .reports import reports_blueprint
    app.register_blueprint(reports_blueprint, url_prefix='/reports')
    from .api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')


def register_logging(app):
    # file logger
    file_handler = RotatingFileHandler('logs/nexus_dashboard.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)


def register_settings(app):
    """Register setting from setting and env

    Args:
        app (Flask): Flask app to register for
    """

    # Load common settings
    try:
        app.config.from_object('app.settings')
    except Exception:
        app.logger.info("No settings.py, loading from example")
        app.config.from_object('app.settings_example')

    # Load environment specific settings
    app.config['TESTING'] = False
    app.config['DEBUG'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_pre_ping": True,
        "pool_size": 10,
        "max_overflow": 2,
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_use_lifo": True
    }

    app.config['SECRET_KEY'] = os.getenv(
        'APP_SECRET_KEY',
        app.config['APP_SECRET_KEY']
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'APP_DATABASE_URI',
        app.config['APP_DATABASE_URI']
    )
    app.config['USER_ENABLE_REGISTER'] = os.getenv(
        'USER_ENABLE_REGISTER',
        app.config['USER_ENABLE_REGISTER']
    )
    app.config['USER_ENABLE_EMAIL'] = os.getenv(
        'USER_ENABLE_EMAIL',
        app.config['USER_ENABLE_EMAIL']
    )
    app.config['USER_ENABLE_CONFIRM_EMAIL'] = os.getenv(
        'USER_ENABLE_CONFIRM_EMAIL',
        app.config['USER_ENABLE_CONFIRM_EMAIL']
    )
    app.config['REQUIRE_PLAY_KEY'] = os.getenv(
        'REQUIRE_PLAY_KEY',
        app.config['REQUIRE_PLAY_KEY']
    )
    app.config['USER_ENABLE_INVITE_USER'] = os.getenv(
        'USER_ENABLE_INVITE_USER',
        app.config['USER_ENABLE_INVITE_USER']
    )
    app.config['USER_REQUIRE_INVITATION'] = os.getenv(
        'USER_REQUIRE_INVITATION',
        app.config['USER_REQUIRE_INVITATION']
    )
    app.config['MAIL_SERVER'] = os.getenv(
        'MAIL_SERVER',
        app.config['MAIL_SERVER']
    )
    app.config['MAIL_PORT'] = int(
        os.getenv(
        'MAIL_PORT',
        app.config['MAIL_PORT']
        )
    )
    app.config['MAIL_USE_SSL'] = os.getenv(
        'MAIL_USE_SSL',
        app.config['MAIL_USE_SSL']
    )
    app.config['MAIL_USE_TLS'] = os.getenv(
        'MAIL_USE_TLS',
        app.config['MAIL_USE_TLS']
    )
    app.config['MAIL_USERNAME'] = os.getenv(
        'MAIL_USERNAME',
        app.config['MAIL_USERNAME']
    )
    app.config['MAIL_PASSWORD'] = os.getenv(
        'MAIL_PASSWORD',
        app.config['MAIL_PASSWORD']
    )
    app.config['USER_EMAIL_SENDER_NAME'] = os.getenv(
        'USER_EMAIL_SENDER_NAME',
        app.config['USER_EMAIL_SENDER_NAME']
    )
    app.config['USER_EMAIL_SENDER_EMAIL'] = os.getenv(
        'USER_EMAIL_SENDER_EMAIL',
        app.config['USER_EMAIL_SENDER_EMAIL']
    )

    if "ENABLE_CHAR_XML_UPLOAD" not in app.config:
        app.config['ENABLE_CHAR_XML_UPLOAD'] = False
    app.config['ENABLE_CHAR_XML_UPLOAD'] = os.getenv(
        'ENABLE_CHAR_XML_UPLOAD',
        app.config['ENABLE_CHAR_XML_UPLOAD']
    )

    if "CLIENT_LOCATION" not in app.config:
        app.config['CLIENT_LOCATION'] = 'app/luclient/'
    app.config['CLIENT_LOCATION'] = os.getenv(
        'CLIENT_LOCATION',
        app.config['CLIENT_LOCATION']
    )

    if "CD_SQLITE_LOCATION" not in app.config:
        app.config['CD_SQLITE_LOCATION'] = 'app/luclient/res/'
    app.config['CD_SQLITE_LOCATION'] = os.getenv(
        'CD_SQLITE_LOCATION',
        app.config['CD_SQLITE_LOCATION']
    )

    if "CACHE_LOCATION" not in app.config:
        app.config['CACHE_LOCATION'] = 'app/cache/'
    app.config['CACHE_LOCATION'] = os.getenv(
        'CACHE_LOCATION',
        app.config['CACHE_LOCATION']
    )

    # Recaptcha settings
    if "RECAPTCHA_ENABLE" not in app.config:
        app.config['RECAPTCHA_ENABLE'] = False
    app.config['RECAPTCHA_ENABLE'] = os.getenv(
        'RECAPTCHA_ENABLE',
        app.config['RECAPTCHA_ENABLE']
    )
    if "RECAPTCHA_PUBLIC_KEY" not in app.config:
        app.config['RECAPTCHA_PUBLIC_KEY'] = ''
    app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv(
        'RECAPTCHA_PUBLIC_KEY',
        app.config['RECAPTCHA_PUBLIC_KEY']
    )
    if "RECAPTCHA_PRIVATE_KEY" not in app.config:
        app.config['RECAPTCHA_PRIVATE_KEY'] = ''
    app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv(
        'RECAPTCHA_PRIVATE_KEY',
        app.config['RECAPTCHA_PRIVATE_KEY']
    )
    # Optional
    if "RECAPTCHA_API_SERVER" in app.config:
        app.config['RECAPTCHA_API_SERVER'] = os.getenv(
            'RECAPTCHA_API_SERVER',
            app.config['RECAPTCHA_API_SERVER']
        )
    if "RECAPTCHA_PARAMETERS" in app.config:
        app.config['RECAPTCHA_PARAMETERS'] = os.getenv(
            'RECAPTCHA_PARAMETERS',
            app.config['RECAPTCHA_PARAMETERS']
        )
    if "RECAPTCHA_DATA_ATTRS" in app.config:
        app.config['RECAPTCHA_DATA_ATTRS'] = os.getenv(
            'RECAPTCHA_DATA_ATTRS',
            app.config['RECAPTCHA_DATA_ATTRS']
        )



def gm_level(gm_level):
    """Decorator for handling permissions based on the user's GM Level

    Args:
        gm_level (int): 0-9
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.gm_level < gm_level:
                return redirect(url_for('main.index'))
            return func(*args, **kwargs)
        return wrapper
    return decorator


def log_audit(message):
    AuditLog(
        account_id=current_user.id,
        action=message
    ).save()
