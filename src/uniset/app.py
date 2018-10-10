import os

from flask import Blueprint
from superset import app, appbuilder

from uniset import ROOT, views
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
