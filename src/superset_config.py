# ---------------------------------------------------------
# Superset specific config
# ---------------------------------------------------------
import os

from flask_appbuilder.security.manager import AUTH_OAUTH

from uniset.config import env

ADMINS = ('s.apostolico@gmail.com',
          'sapostolico@unicef.org',
          )
AUTH_TYPE = AUTH_OAUTH
AUTH_USER_REGISTRATION_ROLE = "Public"
AUTH_USER_REGISTRATION = True

AUTHORITY_URL = 'https://login.microsoftonline.com/nikunicef.onmicrosoft.com'
AUTH_ENDPOINT = '/oauth2/v2.0/authorize'
TOKEN_ENDPOINT = '/oauth2/v2.0/token'
REDIRECT_URI = 'http://localhost:8088/login/authorized'
RESOURCE = 'https://graph.microsoft.com/'
API_VERSION = 'v1.0'
SCOPES = ['User.Read']  # Add other scopes/permissions as needed.
OAUTH_PROVIDERS = [
    {
        'name': 'azure',
        'whitelist': ['@nikunicef.onmicrosoft.com', '@noreply.com'],
        'icon': 'fa-windows',
        'token_key': 'access_token',
        'remote_app': {
            'base_url': RESOURCE + API_VERSION + '/',

            'request_token_url': None,
            # 'access_token_method': 'POST',
            'access_token_url': AUTHORITY_URL + TOKEN_ENDPOINT,
            'authorize_url': AUTHORITY_URL + AUTH_ENDPOINT,
            'request_token_params': {
                'scope': 'user.read openid email profile'
            },
            'consumer_key': env.str('KEY2'),
            'consumer_secret': env.str('SEC2')
        }

    },
    {
        'name': 'google',
        'whitelist': ['@gmail.com'],
        'icon': 'fa-google',
        'token_key': 'access_token',
        'remote_app': {
            'base_url': 'https://www.googleapis.com/oauth2/v2/',
            'request_token_params': {
                'scope': 'email profile'
            },
            'request_token_url': None,
            'access_token_url': 'https://accounts.google.com/o/oauth2/token',
            'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
            'consumer_key': env.str('KK1'),
            'consumer_secret': env.str('SE1')
        }
    }
]

#


ROW_LIMIT = 5000

SUPERSET_WEBSERVER_PORT = 8088
# ---------------------------------------------------------

# ---------------------------------------------------------
# Flask App Builder configuration
# ---------------------------------------------------------
# Your App secret key
SECRET_KEY = os.environ['SECRET_KEY']

# The SQLAlchemy connection string to your database backend
# This connection defines the path to the database that stores your
# superset metadata (slices, connections, tables, dashboards, ...).
# Note that the connection information to connect to the datasources
# you want to explore are managed directly in the web UI
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True
# Add endpoints that need to be exempt from CSRF protection
WTF_CSRF_EXEMPT_LIST = []
# A CSRF token that expires in 1 year
WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365

# Set this API key to enable Mapbox visualizations
MAPBOX_API_KEY = ''
APP_NAME = "UNIset"
APP_THEME = "rph.css"
# APP_THEME = "cyborg.css"       # COOL
# APP_THEME = "spacelab.css"  # NICE
# CUSTOM_SECURITY_MANAGER=UnisetSecurityManager
# ADDON_MANAGERS = ['uniset.manager.UnisetManager']

# CACHE_CONFIG = {
#     'CACHE_TYPE': 'redis',
#     'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24,  # 1 day default (in secs)
#     'CACHE_KEY_PREFIX': 'superset_results',
#     'CACHE_REDIS_URL': 'redis://redis:6379/9',
# }
# MAIL_SERVER = env('MAIL_SERVER')
# MAIL_PORT = 25,
# MAIL_USE_TLS = False,
# MAIL_USE_SSL = False,
# MAIL_DEBUG = False,
# MAIL_USERNAME = '',
# MAIL_PASSWORD = '',
# MAIL_DEFAULT_SENDER = '',
# MAIL_MAX_EMAILS = '',
# MAIL_SUPPRESS_SEND = True,
# MAIL_ASCII_ATTACHMENTS = False
