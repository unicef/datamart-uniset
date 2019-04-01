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
        print(111, "monkeypatch.py:31", 3333333333333333333333333333)
        print(111, "monkeypatch.py:31", userinfo)
        print(111, "monkeypatch.py:31", self.appbuilder.get_app.config['ADMINS'])

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


#
# def oauth_authorized(self, provider):
#     from flask_appbuilder.security.views import (as_unicode, flash, login_user, redirect)
#
#     log.debug("Authorized init")
#     resp = self.appbuilder.sm.oauth_remotes[provider].authorized_response()
#     if resp is None:
#         flash(u'You denied the request to sign in.', 'warning')
#         return redirect('login')
#     log.debug('OAUTH Authorized resp: {0}'.format(resp))
#     # Retrieves specific user info from the provider
#     try:
#         self.appbuilder.sm.set_oauth_session(provider, resp)
#         userinfo = self.appbuilder.sm.oauth_user_info(provider, resp)
#         if not userinfo['email']:
#             raise Exception("User does not have an email. cannot login")
#     except Exception as e:
#         log.error("Error returning OAuth user info: {0}".format(e))
#         user = None
#     else:
#         log.debug("User info retrieved from {0}: {1}".format(provider, userinfo))
#         # User email is not whitelisted
#         if provider in self.appbuilder.sm.oauth_whitelists:
#             whitelist = self.appbuilder.sm.oauth_whitelists[provider]
#             allow = False
#             for e in whitelist:
#                 if re.search(e, userinfo['email']):
#                     allow = True
#                     break
#             if not allow:
#                 flash(u'You are not authorized.', 'warning')
#                 return redirect('login')
#         else:
#             log.debug('No whitelist for OAuth provider')
#         user = self.appbuilder.sm.auth_user_oauth(userinfo)
#
#     if user is None:
#         flash(as_unicode(self.invalid_login_message), 'warning')
#         return redirect('login')
#     else:
#         login_user(user)
#         return redirect(self.appbuilder.get_url_for_index)


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
        if 1 in self.applied:
            return
        self.applied.append(1)
        from flask_appbuilder import base
        base.dynamic_class_import = dynamic_class_import

    def patch2(self, appbuilder):
        if 2 in self.applied:
            return
        self.applied.append(2)

        from superset import app  # noqa
        from uniset import views  # noqa

        # # Azure support
        # from flask_appbuilder.security.views import AuthOAuthView
        #
        # auth_view = [o for o in appbuilder.baseviews if isinstance(o, AuthOAuthView)]
        # if auth_view:
        #     mth = types.MethodType(oauth_authorized, auth_view[0])
        #     auth_view[0].oauth_authorized = mth
        #     app.view_functions['AuthOAuthView.oauth_authorized'] = mth

        # appbuilder.baseviews = [o for o in appbuilder.baseviews if not isinstance(o, AuthOAuthView)]
        # v = appbuilder.add_view_no_menu(OAuthView)
        # appbuilder.sm.auth_view = v
        # app.view_functions['AuthOAuthView.oauth_authorized'] = v.oauth_authorized
        # app.view_functions['AuthOAuthView.login'] = v.login

        # we cannot override SecurityManager / monkeypatch what we need
        # Existing user support/merge
        # from uniset.security import UnisetSecurityManager
        # am = UnisetSecurityManager(appbuilder)
        mth = types.MethodType(auth_user_oauth, appbuilder.sm)
        appbuilder.sm.auth_user_oauth = mth


patcher = Patcher()
