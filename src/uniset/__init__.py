import os

import flask_appbuilder.base

VERSION = __version__ = '1.0'
NAME = 'uniset'

ROOT = os.path.dirname(__file__)


def dynamic_class_import(class_path):
    """
        Will dynamically import a class from a string path
        :param class_path: string with class path
        :return: class
    """
    # Split first occurrence of path
    from functools import reduce
    try:
        tmp = class_path.split('.')
        module_path = '.'.join(tmp[0:-1])
        package = __import__(module_path)
        return reduce(getattr, tmp[1:], package)
    except Exception as e:
        flask_appbuilder.base.log.exception(e)
        flask_appbuilder.base.log.error(flask_appbuilder.base.LOGMSG_ERR_FAB_ADDON_IMPORT.format(class_path, e))


flask_appbuilder.base.dynamic_class_import = dynamic_class_import
