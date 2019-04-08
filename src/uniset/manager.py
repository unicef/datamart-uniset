import logging
import os

from flask_appbuilder.basemanager import BaseManager

from flask import Blueprint

from uniset import ROOT

log = logging.getLogger(__name__)


class UnisetManager(BaseManager):

    def __init__(self, appbuilder):
        super(UnisetManager, self).__init__(appbuilder)
        appbuilder.app.jinja_loader.searchpath.insert(0, os.path.join(ROOT, 'templates'))

    def register_views(self):
        bp = Blueprint('uniset', __name__, url_prefix='/static',
                       template_folder='templates',
                       static_folder=os.path.join(ROOT, 'static'),
                       static_url_path='/uniset')

        self.appbuilder.get_app.register_blueprint(bp)

        from uniset.jinja import context_processors  # noqa
        from uniset.views.users import LoadUserView

        self.appbuilder.add_separator('Security')

        self.appbuilder.add_view(LoadUserView,
                                 "Load users",
                                 icon="fa-cloud-download",
                                 category="Security",
                                 category_icon="fa-envelope")

        # self.appbuilder.add_view(UserProfileView,
        #                          "User profiles",
        #                          icon="fa-user-circle",
        #                          category="Security",
        #                          category_icon="fa-cloud-download-alt")

        # from .monkeypatch import patcher
        # patcher.patch2(self.appbuilder)
        # from uniset.azure.jwt import _azure_jwt_token_parse
        #
        # @self.appbuilder.sm.oauth_user_info_getter
        # def my_oauth_user_info(sm, provider, response):
        #     from flask_appbuilder.security.manager import log
        #     if provider == 'google':
        #         me = sm.oauth_remotes[provider].get('userinfo')
        #         log.debug("User info from Google: {0}".format(me.data))
        #         return {'username': "google_" + me.data.get('id', ''),
        #                 'first_name': me.data.get('given_name', ''),
        #                 'last_name': me.data.get('family_name', ''),
        #                 'email': me.data.get('email', '')}
        #
        #     if provider == 'azure':
        #         log.debug("Azure response received : {0}".format(response))
        #         id_token = response['id_token']
        #         log.debug(str(id_token))
        #         me = _azure_jwt_token_parse(id_token)
        #         log.debug("Parse JWT token : {0}".format(me))
        #         gres = sm.oauth_remotes[provider].get('users/%s' % me['oid'])
        #         log.debug("MSGraph infos: {0}".format(gres.data))
        #         me.update(gres.data)
        #         fake_email = '%s@noreply.com' % me['oid']
        #         return {'name': me['displayName'],
        #                 'email': me.get('mail', fake_email) or fake_email,
        #                 'first_name': me['givenName'],
        #                 'last_name': me['surname'],
        #                 'id': me['oid'],
        #                 'username': me['oid']}
        #
        #     else:
        #         return {}
