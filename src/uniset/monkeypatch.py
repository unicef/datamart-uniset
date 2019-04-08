import logging
import types

# from superset import SupersetSecurityManager

log = logging.getLogger(__name__)


def auth_user_oauth(self, userinfo):
    from flask_appbuilder.const import LOGMSG_WAR_SEC_LOGIN_FAILED

    if 'username' in userinfo:
        user = self.find_user(username=userinfo['username'])
    elif 'email' in userinfo:
        user = self.find_user(email=userinfo['email'])
    else:
        log.error('User info does not have username or email {0}'.format(userinfo))
        return None

    # User is disabled
    if user and not user.is_active:
        log.info(LOGMSG_WAR_SEC_LOGIN_FAILED.format(userinfo))
        return None

    # If user does not exist on the DB and not self user registration, go away
    if not user and not self.auth_user_registration:
        return None
    # User does not exist, create one if self registration.
    if not user:
        # TODO: remove me
        if (userinfo['email'] in self.appbuilder.get_app.config['ADMINS'] or
                userinfo.get('name') in self.appbuilder.get_app.config['ADMINS']):
            role = self.find_role('Admin')
        else:
            role = self.find_role(self.auth_user_registration_role)

        user = self.add_user(
            username=userinfo['username'],
            first_name=userinfo['first_name'],
            last_name=userinfo['last_name'],
            email=userinfo['email'],
            role=role
        )
        if not user:
            log.error("Error creating a new OAuth user %s" % userinfo['username'])
            return None
    self.update_user_auth_stat(user)
    return user


auth_user_oauth.patched = True


def dynamic_class_import(class_path):
    from functools import reduce
    from flask_appbuilder import base

    try:
        tmp = class_path.split('.')
        module_path = '.'.join(tmp[0:-1])
        package = __import__(module_path)
        return reduce(getattr, tmp[1:], package)
    except Exception as e:
        base.log.exception(e)
        base.log.error(base.LOGMSG_ERR_FAB_ADDON_IMPORT.format(class_path, e))


dynamic_class_import.patched = True


class Patcher:
    applied = []

    def patch1(self):
        # fix for 'NameError: name 'reduce' is not defined'
        # for python 3.6
        if 1 in self.applied:
            return
        self.applied.append(1)
        from flask_appbuilder import base
        base.dynamic_class_import = dynamic_class_import

    def patch2(self, appbuilder):
        if 2 in self.applied:
            return
        # self.applied.append(2)
        #
        # from superset import app  # noqa
        # from uniset import views  # noqa
        #
        # mth = types.MethodType(auth_user_oauth, appbuilder.sm)
        # appbuilder.sm.auth_user_oauth = mth


patcher = Patcher()
