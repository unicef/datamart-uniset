import logging

from superset import appbuilder, SupersetSecurityManager

from uniset.azure.jwt import _azure_jwt_token_parse

log = logging.getLogger(__name__)


class UnisetSecurityManager(SupersetSecurityManager):

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
            if userinfo['email'] in self.appbuilder.get_app.config['ADMINS']:
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


@appbuilder.sm.oauth_user_info_getter
def my_oauth_user_info(sm, provider, response):
    from flask_appbuilder.security.manager import log
    if provider == 'google':
        me = sm.oauth_remotes[provider].get('userinfo')
        log.debug("User info from Google: {0}".format(me.data))
        return {'username': "google_" + me.data.get('id', ''),
                'first_name': me.data.get('given_name', ''),
                'last_name': me.data.get('family_name', ''),
                'email': me.data.get('email', '')}

    if provider == 'azure':
        log.debug("Azure response received : {0}".format(response))
        id_token = response['id_token']
        log.debug(str(id_token))
        me = _azure_jwt_token_parse(id_token)
        log.debug("Parse JWT token : {0}".format(me))
        gres = sm.oauth_remotes[provider].get('users/%s' % me['oid'])
        log.debug("MSGraph infos: {0}".format(gres.data))
        me.update(gres.data)
        fake_email = '%s@noreply.com' % me['oid']
        return {'name': me['displayName'],
                'email': me.get('mail', fake_email) or fake_email,
                'first_name': me['givenName'],
                'last_name': me['surname'],
                'id': me['oid'],
                'username': me['oid']}

    else:
        return {}
