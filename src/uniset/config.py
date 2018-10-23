from uniset.environ import Env

DEFAULTS = dict(
    GOOGLE_CLIENT_ID="",
    GOOGLE_CLIENT_SECRET="",
    AZURE_CLIENT_ID="",
    AZURE_CLIENT_SECRET="",

    CACHE_REDIS_URL='redis://127.0.0.1:6379/9',

    CELERY_BROKER_URL='redis://127.0.0.1:6379/0',
    CELERY_RESULT_BACKEND='redis://127.0.0.1:6379/0',

    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=25,
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=False,
    MAIL_DEBUG=False,
    MAIL_USERNAME='',
    MAIL_PASSWORD='',
    MAIL_DEFAULT_SENDER='',
    MAIL_MAX_EMAILS='',
    MAIL_SUPPRESS_SEND=True,
    MAIL_ASCII_ATTACHMENTS=False
)

env = Env(defaults=DEFAULTS)
