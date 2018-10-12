import os

from flask_appbuilder.security.views import AuthOAuthView

from flask import Blueprint

from uniset import ROOT
from uniset.azure.jwt import _azure_jwt_token_parse
from uniset.monkeypatch import AuthOAuthView2


def setup():
    from superset import app, appbuilder
    from uniset import views

    appbuilder.baseviews = [o for o in appbuilder.baseviews if not isinstance(o, AuthOAuthView)]
    v = appbuilder.add_view_no_menu(AuthOAuthView2)
    appbuilder.sm.auth_view = v
    app.view_functions['AuthOAuthView.oauth_authorized'] = v.oauth_authorized
    app.view_functions['AuthOAuthView.login'] = v.login

    from uniset.jinja import context_processors  # noqa
    app.jinja_loader.searchpath.insert(0, os.path.join(ROOT, 'templates'))
    bp = Blueprint('uniset', __name__, url_prefix='/static',
                   template_folder='templates',
                   static_folder=os.path.join(ROOT, 'static'),
                   static_url_path='/uniset')

    appbuilder.get_app.register_blueprint(bp)
    appbuilder.add_separator('Security')

    appbuilder.add_view(views.LoadUserView,
                        "Load users",
                        icon="fa-cloud-download",
                        category="Security",
                        category_icon="fa-envelope")

    appbuilder.add_view(views.UserProfileView,
                        "User profiles",
                        icon="fa-user-circle",
                        category="Security",
                        category_icon="fa-cloud-download-alt")

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
            # {'aud': 'fca9cbcc-7e62-48e0-b7a0-b680cebd7455',
            #  'iss': 'https://login.microsoftonline.com/bee9ee22-4873-461b-82a3-ce2a536d7c62/v2.0',
            #  'iat': 1539361103,
            #  'nbf': 1539361103,
            #  'exp': 1539365003,
            #  'ageGroup': '3',
            #  'aio': 'ATQAy/8JAAAACd4TDuF+VEJH3NFHy9dZYr3WeQC6i4ovRuL7rGq2wvmTqkrUIOaSfVkDmmEOeJZy',
            #  'name': 'Stefano Apostolico',
            #  'oid': 'da13bd43-4586-444e-a9d1-7e6e96d3126f',
            #  'preferred_username': 'sapostolico@nikunicef.onmicrosoft.com',
            #  'sub': '2uISonZJfyQYzpX-u2ZgOORzJAVJsHx3JwBoAMd65Ik',
            #  'tid': 'bee9ee22-4873-461b-82a3-ce2a536d7c62',
            #  'uti': 'ndZ-Hws71UWQktPj8FeGAA', 'ver': '2.0'}
            gres = sm.oauth_remotes[provider].get('users/%s' % me['oid'])
            log.debug("MSGraph infos: {0}".format(gres.data))
            # {'@odata.context': 'https://graph.microsoft.com/v1.0/$metadata#users/$entity',
            #  'id': 'da13bd43-4586-444e-a9d1-7e6e96d3126f',
            #  'businessPhones': ['+1 123'],
            #  'displayName': 'Stefano Apostolico',
            #  'givenName': 'Stefano',
            #  'jobTitle': 'TA',
            #  'mail': None,
            #  'mobilePhone': '+1 123',
            #  'officeLocation': 'asda',
            #  'preferredLanguage': 'en-GB',
            #  'surname': 'Apostolico',
            #  'userPrincipalName': 'sapostolico@nikunicef.onmicrosoft.com'}
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

    return app


app = setup()
