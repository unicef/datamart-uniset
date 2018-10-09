# ---------------------------------------------------------
# Superset specific config
# ---------------------------------------------------------
import os

from uniset.security import UnisetSecurityManager

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
# CUSTOM_SECURITY_MANAGER = UnisetSecurityManager

ADDON_MANAGERS = ['uniset.manager.UnisetManager']

# CACHE_CONFIG = {
#     'CACHE_TYPE': 'redis',
#     'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24,  # 1 day default (in secs)
#     'CACHE_KEY_PREFIX': 'superset_results',
#     'CACHE_REDIS_URL': 'redis://redis:6379/9',
# }
