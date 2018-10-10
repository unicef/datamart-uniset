# from flask_appbuilder.security.sqla.manager import SecurityManager
# from flask_appbuilder.security.sqla.models import User
# from superset import SupersetSecurityManager
#
#
# class UnisetSecurityManager(SupersetSecurityManager):
#     user_model = User
#
#     def can_access(self, permission_name, view_name, user=None):
#         # TODO: remove me
#         print(111, "security.py:11", permission_name)
#         return super(UnisetSecurityManager, self).can_access(permission_name, view_name, user)
#
