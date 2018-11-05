# ---------------------------------------------------------
# Superset specific config
# ---------------------------------------------------------
import os

from flask_appbuilder.security.manager import AUTH_OAUTH

from uniset.settings import env

ADMINS = ('s.apostolico@gmail.com',
          'sapostolico@unicef.org',
          'sapostolico@nikunicef.onmicrosoft.com',
          'sapostolico@saxix.onmicrosoft.com',
          'da13bd43-4586-444e-a9d1-7e6e96d3126f@noreply.com',
          '94501d3a-8346-4872-948c-82bce9e514b4@noreply.com',
          )

AUTH_TYPE = AUTH_OAUTH
AUTH_USER_REGISTRATION_ROLE = "Public"
AUTH_USER_REGISTRATION = True

AUTHORITY_URL = 'https://login.microsoftonline.com/' + env('AUTHORITY_URL')
AUTH_ENDPOINT = '/oauth2/v2.0/authorize'
TOKEN_ENDPOINT = '/oauth2/v2.0/token'
REDIRECT_URI = 'http://localhost:8088/login/authorized'
RESOURCE = 'https://graph.microsoft.com/'
API_VERSION = 'v1.0'
SCOPES = ['User.Read']  # Add other scopes/permissions as needed.
OAUTH_PROVIDERS = [
    {
        'name': 'azure',
        'whitelist': ['@saxix.onmicrosoft.com', '@noreply.com'],
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
            'consumer_key': env.str('AZURE_CLIENT_ID'),
            'consumer_secret': env.str('AZURE_CLIENT_SECRET')
        }

    },
    #     # {
    #     #     'name': 'google',
    #     #     'whitelist': ['@gmail.com'],
    #     #     'icon': 'fa-google',
    #     #     'token_key': 'access_token',
    #     #     'remote_app': {
    #     #         'base_url': 'https://www.googleapis.com/oauth2/v2/',
    #     #         'request_token_params': {
    #     #             'scope': 'email profile'
    #     #         },
    #     #         'request_token_url': None,
    #     #         'access_token_url': 'https://accounts.google.com/o/oauth2/token',
    #     #         'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
    #     #         'consumer_key': env.str('GOOGLE_CLIENT_KEY'),
    #     #         'consumer_secret': env.str('GOOGLE_CLIENT_SECRET')
    #     #     }
    #     # }
]
#
# #
#
#
# ROW_LIMIT = 5000
#
SUPERSET_WEBSERVER_PORT = 8088
# # ---------------------------------------------------------
#
# # ---------------------------------------------------------
# # Flask App Builder configuration
# # ---------------------------------------------------------
# # Your App secret key
SECRET_KEY = env('SECRET_KEY')
#
# # The SQLAlchemy connection string to your database backend
# # This connection defines the path to the database that stores your
# # superset metadata (slices, connections, tables, dashboards, ...).
# # Note that the connection information to connect to the datasources
# # you want to explore are managed directly in the web UI
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
#
# # Flask-WTF flag for CSRF
# WTF_CSRF_ENABLED = True
# # Add endpoints that need to be exempt from CSRF protection
# WTF_CSRF_EXEMPT_LIST = []
# # A CSRF token that expires in 1 year
# WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365
#
# # Set this API key to enable Mapbox visualizations
MAPBOX_API_KEY = env('MAPBOX_API_KEY')

APP_NAME = "uniset"
# # APP_THEME = "rph.css"
# # APP_THEME = "united.css"       # COOL
# APP_THEME = "simplex.css"  # NICE
# from uniset.security import UnisetSecurityManager
# CUSTOM_SECURITY_MANAGER = UnisetSecurityManager
ADDON_MANAGERS = ['uniset.manager.UnisetManager']

CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24,  # 1 day default (in secs)
    'CACHE_KEY_PREFIX': 'uniset',
    'CACHE_REDIS_URL': env('CACHE_REDIS_URL'),
}

MAIL_SERVER = env('MAIL_SERVER')
MAIL_PORT = env('MAIL_PORT')
MAIL_USE_TLS = env('MAIL_USE_TLS')
MAIL_USE_SSL = env('MAIL_USE_SSL')
MAIL_DEBUG = env('MAIL_DEBUG')
MAIL_USERNAME = env('MAIL_USERNAME')
MAIL_PASSWORD = env('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = env('MAIL_DEFAULT_SENDER')
MAIL_MAX_EMAILS = env('MAIL_MAX_EMAILS')
MAIL_SUPPRESS_SEND = env('MAIL_SUPPRESS_SEND')
MAIL_ASCII_ATTACHMENTS = env('MAIL_ASCII_ATTACHMENTS')


class CeleryConfig(object):
    BROKER_URL = env('CELERY_BROKER_URL')
    CELERY_IMPORTS = ('superset.sql_lab',)
    CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')
    CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}


CELERY_CONFIG = CeleryConfig
