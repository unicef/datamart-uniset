from uniset.environ import Env

DEFAULTS = dict(
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
