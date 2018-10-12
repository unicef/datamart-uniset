import logging
import re

from flask_appbuilder.security.views import (AuthOAuthView, as_unicode, expose,
                                             flash, login_user, redirect,)

log = logging.getLogger(__name__)


class AuthOAuthView2(AuthOAuthView):
    @expose('/oauth-authorized/<provider>')
    def oauth_authorized(self, provider):
        log.debug("Authorized init")
        resp = self.appbuilder.sm.oauth_remotes[provider].authorized_response()
        if resp is None:
            flash(u'You denied the request to sign in.', 'warning')
            return redirect('login')
        log.debug('OAUTH Authorized resp: {0}'.format(resp))
        # Retrieves specific user info from the provider
        try:
            self.appbuilder.sm.set_oauth_session(provider, resp)
            userinfo = self.appbuilder.sm.oauth_user_info(provider, resp)
            if not userinfo['email']:
                raise Exception("User does not have an email. cannot login")
        except Exception as e:
            log.error("Error returning OAuth user info: {0}".format(e))
            user = None
        else:
            log.debug("User info retrieved from {0}: {1}".format(provider, userinfo))
            # User email is not whitelisted
            if provider in self.appbuilder.sm.oauth_whitelists:
                whitelist = self.appbuilder.sm.oauth_whitelists[provider]
                allow = False
                for e in whitelist:
                    if re.search(e, userinfo['email']):
                        allow = True
                        break
                if not allow:
                    flash(u'You are not authorized.', 'warning')
                    return redirect('login')
            else:
                log.debug('No whitelist for OAuth provider')
            user = self.appbuilder.sm.auth_user_oauth(userinfo)

        if user is None:
            flash(as_unicode(self.invalid_login_message), 'warning')
            return redirect('login')
        else:
            login_user(user)
            return redirect(self.appbuilder.get_url_for_index)
