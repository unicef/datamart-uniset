import logging
import os
import re

logger = logging.getLogger(__name__)


class ImproperlyConfigured(Exception):
    pass


class NoValue(object):

    def __repr__(self):
        return '<{0}>'.format(self.__class__.__name__)


class Env(object):
    ENVIRON = os.environ
    NOTSET = NoValue()
    BOOLEAN_TRUE_STRINGS = ('true', 'on', 'ok', 'y', 'yes', '1', '+')

    def __init__(self, env_file=None, debug=False, prefix='', lazy=False,
                 defaults=None):
        self.env_file = env_file
        self.prefix = prefix
        self.lazy = lazy
        self.debug = debug
        self.scheme = defaults
        if not self.lazy:
            self.read_env()

    def __getattr__(self, var):
        return self.get_value(var)

    def __call__(self, var, cast=None, default=NOTSET, parse_default=False):
        return self.get_value(var, cast=cast, default=default, parse_default=parse_default)

    def __contains__(self, var):
        return var in self.ENVIRON

    # Shortcuts

    def str(self, var, default=NOTSET, multiline=False):
        """
        :rtype: str
        """
        value = self.get_value(var, default=default)
        if multiline:
            return value.replace('\\n', '\n')
        return value

    def bytes(self, var, default=NOTSET, encoding='utf8'):
        """
        :rtype: bytes
        """
        return self.get_value(var, cast=str).encode(encoding)

    def bool(self, var, default=NOTSET):
        """
        :rtype: bool
        """
        return self.get_value(var, cast=bool, default=default)

    def int(self, var, default=NOTSET):
        """
        :rtype: int
        """
        return self.get_value(var, cast=int, default=default)

    def float(self, var, default=NOTSET):
        """
        :rtype: float
        """
        return self.get_value(var, cast=float, default=default)

    def get_value(self, var, cast=None, default=NOTSET,  # noqa: C901
                  parse_default=False, raw=False):
        """Return value for given environment variable.

                :param var: Name of variable.
                :param cast: Type to cast return value as.
                :param default: If var not present in environ, return this instead.
                :param parse_default: force to parse default..

                :returns: Value from environment or default (if set)
                """

        if raw:
            env_var = var
        else:
            env_var = self.prefix + var

        # logger.debug(f"get '{env_var}' casted as '{cast}' with default '{default}'")

        if var in self.scheme:
            var_info = self.scheme[var]

            try:
                has_default = len(var_info) == 2
            except TypeError:
                has_default = False

            if has_default:
                if not cast:
                    cast = var_info[0]

                if default is self.NOTSET:
                    try:
                        default = var_info[1]
                    except IndexError:
                        pass
            else:
                if not cast:
                    cast = var_info

        try:
            value = self.ENVIRON[env_var]
        except KeyError:
            if default is self.NOTSET:
                error_msg = "Set the {} environment variable".format(env_var)
                raise ImproperlyConfigured(error_msg)

            value = default

        # Resolve any proxied values
        if hasattr(value, 'startswith') and '${' in value:
            m = re.search(r'(\${(.*?)})', value)
            while m:
                value = re.sub(re.escape(m.group(1)), self.get_value(m.group(2), raw=True), value)
                m = re.search(r'(\${(.*?)})', value)

        if value != default or (parse_default and value):
            value = self.parse_value(value, cast)

        logger.debug("get '{}' returns '{}'".format(var, value))
        return value

    # Class and static methods

    @classmethod  # noqa: C901
    def parse_value(cls, value, cast):
        """Parse and cast provided value

        :param value: Stringed value.
        :param cast: Type to cast return value as.

        :returns: Casted value
        """
        if cast is None:
            return value
        elif cast is bool:
            try:
                value = int(value) != 0
            except ValueError:
                value = value.lower() in cls.BOOLEAN_TRUE_STRINGS
        elif isinstance(cast, list):
            value = list(map(cast[0], [x for x in value.split(',') if x]))
        elif isinstance(cast, tuple):
            val = value.strip('(').strip(')').split(',')
            value = tuple(map(cast[0], [x for x in val if x]))
        elif isinstance(cast, dict):
            key_cast = cast.get('key', str)
            value_cast = cast.get('value', str)
            value_cast_by_key = cast.get('cast', dict())
            value = dict(map(
                lambda kv: (
                    key_cast(kv[0]),
                    cls.parse_value(kv[1], value_cast_by_key.get(kv[0], value_cast))
                ),
                [val.split('=') for val in value.split(';') if val]
            ))
        elif cast is dict:
            value = dict([val.split('=') for val in value.split(',') if val])
        elif cast is list:
            value = [x for x in value.split(',') if x]
        elif cast is tuple:
            val = value.strip('(').strip(')').split(',')
            value = tuple([x for x in val if x])
        elif cast is float:
            # clean string
            float_str = re.sub(r'[^\d,\.]', '', value)
            # split for avoid thousand separator and different locale comma/dot symbol
            parts = re.split(r'[,\.]', float_str)
            if len(parts) == 1:
                float_str = parts[0]
            else:
                float_str = "{0}.{1}".format(''.join(parts[0:-1]), parts[-1])
            value = float(float_str)
        else:
            value = cast(value)
        return value

    def get_content(self):
        if self.env_file is None:
            self.env_file = os.environ.get('ENV_FILE', os.path.join(os.curdir, '.env'))

        if hasattr(self.env_file, 'read'):
            content = self.env_file.read()
        elif os.path.exists(self.env_file):
            with open(self.env_file) as f:
                content = f.read()
        else:
            # warnings.warn(
            #     "%s doesn't exist - if you're not configuring your "
            #     "environment separately, create one." % self.env_file,
            #     stacklevel=0)
            content = ''
        logger.debug('Read environment variables from: {0}'.format(self.env_file))
        return content

    def read_env(self):
        content = self.get_content()
        dot_values = {}
        for line in content.splitlines():
            m1 = re.match(r'\A(?:export )?([A-Za-z_0-9]+)=(.*)\Z', line)
            if m1:
                key, val = m1.group(1), m1.group(2)
                m2 = re.match(r"\A'(.*)'\Z", val)
                if m2:
                    val = m2.group(1)
                m3 = re.match(r'\A"(.*)"\Z', val)
                if m3:
                    val = re.sub(r'\\(.)', r'\1', m3.group(1))
                if key in self.scheme:
                    dot_values[key] = str(val)
                    # self.ENVIRON.setdefault(key, str(val))

        # set defaults
        # for key, value in overrides.items():
        #     cls.ENVIRON.setdefault(key, value)
        #
        for key, value in self.scheme.items():
            if isinstance(value, (list, tuple)):
                cast, default = value
            else:
                cast = type(value)
                default = value
                self.scheme[key] = (cast, default)
            os.environ.setdefault(key, dot_values.get(key, str(default)))
            #
            # os.environ.setdefault(key, str(default))
