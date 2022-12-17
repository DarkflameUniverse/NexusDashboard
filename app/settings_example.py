# Settings common to all environments (development|staging|production)

# Application settings
APP_NAME = "Nexus Dashboard"
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"

APP_SECRET_KEY = ""
APP_DATABASE_URI = "mysql+pymysql://<username>:<password>@<host>:<port>/<database>"

CLIENT_LOCATION = 'app/luclient/'
CD_SQLITE_LOCATION = 'app/luclient/res/'
CACHE_LOCATION = 'app/cache/'

CONFIG_LINK = False
CONFIG_LINK_TITLE = ""
CONFIG_LINK_HREF = ""
CONFIG_LINK_TEXT = ""

# Send Analytics for Developers to better fix issues
ALLOW_ANALYTICS = False

# Flask settings
CSRF_ENABLED = True

# Flask-SQLAlchemy settings
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_TIME_LIMIT = 86400

# Flask-User settings
USER_APP_NAME = APP_NAME
USER_ENABLE_CHANGE_PASSWORD = True  # Allow users to change their password
USER_ENABLE_CHANGE_USERNAME = False  # Allow users to change their username
USER_ENABLE_REGISTER = False  # Allow new users to register

# Should alwyas be set to true
USER_REQUIRE_RETYPE_PASSWORD = True  # Prompt for `retype password`
USER_ENABLE_USERNAME = True  # Register and Login with username

# Email Related Settings
USER_ENABLE_EMAIL = False  # Register with Email WILL - DISABLE OTHER THINGS TOO
USER_ENABLE_CONFIRM_EMAIL = True  # Force users to confirm their email
USER_ENABLE_INVITE_USER = False  # Allow users to be invited
USER_REQUIRE_INVITATION = False  # Only invited users may - WILL DISABLE REGISTRATION
USER_ENABLE_FORGOT_PASSWORD = True  # Allow users to reset their passwords

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_USERNAME = None
MAIL_PASSWORD = None
USER_EMAIL_SENDER_NAME = None
USER_EMAIL_SENDER_EMAIL = None

# Require Play Key
REQUIRE_PLAY_KEY = True

# Password hashing settings DO NOT CHANGE
USER_PASSLIB_CRYPTCONTEXT_SCHEMES = ['bcrypt']  # bcrypt for password hashing

# Flask-User routing settings
USER_AFTER_LOGIN_ENDPOINT = "main.index"
USER_AFTER_LOGOUT_ENDPOINT = "main.index"

# Option will be removed once this feature is full implemeted
ENABLE_CHAR_XML_UPLOAD = False
