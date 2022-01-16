# Settings common to all environments (development|staging|production)

# Application settings
APP_NAME = "Nexus Dashboard"
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"

# Flask settings
CSRF_ENABLED = True

# Flask-SQLAlchemy settings
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_TIME_LIMIT = 86400

# Flask-User settings
USER_APP_NAME = APP_NAME
USER_ENABLE_CHANGE_PASSWORD = True  # Allow users to change their password
USER_ENABLE_CHANGE_USERNAME = True  # Allow users to change their username
USER_ENABLE_REGISTER = False  # Allow new users to register

# Should alwyas be set to true
USER_REQUIRE_RETYPE_PASSWORD = True  # Prompt for `retype password`
USER_ENABLE_USERNAME = True  # Register and Login with username

# Email Related Settings
USER_ENABLE_EMAIL = True  # Register with Email WILL - DISABLE OTHER THINGS TOO
USER_ENABLE_CONFIRM_EMAIL = True  # Force users to confirm their email
USER_ENABLE_INVITE_USER = False  # Allow users to be invited
USER_REQUIRE_INVITATION = False  # Only invited users may - WILL DISABLE REGISTRATION
USER_ENABLE_FORGOT_PASSWORD = True  # Allow users to reset their passwords

# Require Play Key
REQUIRE_PLAY_KEY = True

# Password hashing settings
USER_PASSLIB_CRYPTCONTEXT_SCHEMES = ['bcrypt']  # bcrypt for password hashing

# Flask-User routing settings
USER_AFTER_LOGIN_ENDPOINT = "main.index"
USER_AFTER_LOGOUT_ENDPOINT = "main.index"
