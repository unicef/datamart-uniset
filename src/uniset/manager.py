# import logging
# import os
# import superset
#
# from flask import Blueprint
# from flask_appbuilder.basemanager import BaseManager
# from uniset import ROOT
# from uniset.security import UnisetSecurityManager
#
# log = logging.getLogger(__name__)
#
#
# class UnisetManager(BaseManager):
#
#     def __init__(self, appbuilder):
#         super(UnisetManager, self).__init__(appbuilder)
#         appbuilder.app.jinja_loader.searchpath.insert(0, os.path.join(ROOT, 'templates'))
#         # TODO: remove me
#         print(111, "manager.py:19", 99999)
#
#
#     def register_views(self):
#         bp = Blueprint('uniset', __name__, url_prefix='/static',
#                        template_folder='templates',
#                        static_folder=os.path.join(ROOT, 'static'),
#                        static_url_path='/uniset')
#
#         # self.appbuilder.get_app.register_blueprint(bp)
#         from uniset.jinja import context_processors  # noqa
#         from uniset.views.users import LoadUserView, UserProfileView
#
#         self.appbuilder.add_separator('Security')
#
#         self.appbuilder.add_view(LoadUserView,
#                             "Load users",
#                             icon="fa-cloud-download",
#                             category="Security",
#                             category_icon="fa-envelope")
#
#         self.appbuilder.add_view(UserProfileView,
#                             "User profiles",
#                             icon="fa-user-circle",
#                             category="Security",
#                             category_icon="fa-cloud-download-alt")
#
#     def pre_process(self):
#         print(111, "manager.py:19", 88888)
#         # # FIXME: pdb
#         # import pdb; pdb.set_trace()
#         # sm = UnisetSecurityManager(self.appbuilder)
#         #
#         # self.appbuilder.security_manager_class = UnisetSecurityManager
#         # self.appbuilder.sm = sm
#         # superset.security_manager = sm
#
#     def post_process(self):
#         pass
