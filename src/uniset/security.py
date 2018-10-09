from flask_appbuilder.security.sqla.manager import SecurityManager
from superset import SupersetSecurityManager

from .models import UnisetUser
from .views.users import UnisetUserDBModelView


class UnisetSecurityManager(SupersetSecurityManager):
    user_model = UnisetUser
    userdbmodelview = UnisetUserDBModelView
