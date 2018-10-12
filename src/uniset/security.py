# from superset import SupersetSecurityManager
#
# from uniset.monkeypatch import OAuthView
#
#
# class UnisetSecurityManager(SupersetSecurityManager):
#     authoauthview = OAuthView
#     def __init__(self, appbuilder):
#         super().__init__(appbuilder)
#         self.__class__ = SupersetSecurityManager
#
#     def can_access(self, permission_name, view_name, user=None):
#         return super(UnisetSecurityManager, self).can_access(permission_name, view_name, user)
#
