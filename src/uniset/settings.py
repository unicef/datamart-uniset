from uniset.environ import Env

DEFAULTS = dict(
    AUTHORITY_URL='unicef.org',
    AZURE_CLIENT_ID="",
    AZURE_CLIENT_SECRET="",

    CACHE_REDIS_URL='redis://127.0.0.1:6379/9',

    CELERY_BROKER_URL='redis://127.0.0.1:6379/0',
    CELERY_RESULT_BACKEND='redis://127.0.0.1:6379/0',
    MAPBOX_API_KEY='',

    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=25,
    MAIL_USE_TLS=(bool, False),
    MAIL_USE_SSL=(bool, False),
    MAIL_DEBUG=(bool, False),
    MAIL_USERNAME='',
    MAIL_PASSWORD='',
    MAIL_DEFAULT_SENDER='',
    MAIL_MAX_EMAILS='',
    MAIL_SUPPRESS_SEND=(bool, True),
    MAIL_ASCII_ATTACHMENTS=(bool, False),
    SENTRY_DSN=(str, ''),

)

env = Env(defaults=DEFAULTS)
