from flask import flash
from flask_appbuilder.fieldwidgets import BS3TextAreaFieldWidget
from flask_appbuilder.forms import DynamicForm
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.security.sqla.models import User
from flask_appbuilder import ModelView, expose, has_access, SimpleFormView
from superset import appbuilder, db
from wtforms import StringField
from wtforms.validators import DataRequired

from uniset.azure.synchronizer import Synchronizer, SyncResult
from uniset.models import UserProfile


class LoadUserForm(DynamicForm):
    emails = StringField('Emails',
                         description=('Enter part of email/username separated by comma'),
                         validators=[DataRequired()], widget=BS3TextAreaFieldWidget())


class UnisetSynchronizer(Synchronizer):
    def _store(self, pk, values):
        created = False
        datamodel = SQLAInterface(User, db.session)
        P = SQLAInterface(UserProfile, db.session)
        u = db.session.query(User).filter_by(email=values['email']).first()
        if not u:
            created = True
            u = User(first_name=values['first_name'],
                     last_name=values['last_name'],
                     email=values['email'],
                     username=values['email'],
                     active=False)
            datamodel.add(u)
        else:
            datamodel.add(u)
        if u.profiles:
            profile = u.profiles[0]
            profile.uuid = values['azure_id']
        else:
            profile = UserProfile(user_id=u.id)
            profile.uuid = values['azure_id']
        P.add(profile)
        return values, created


class LoadUserView(SimpleFormView):
    route_base = "/users"
    form = LoadUserForm
    message = 'My form submitted'

    def form_get(self, form):
        form.emails.data = 'ddinicola'

    def form_post(self, form):
        try:
            synchronizer = UnisetSynchronizer()
            emails = form.data['emails'].split(',')
            total_results = SyncResult()
            for email in emails:
                result = synchronizer.fetch_users("startswith(mail,'%s')" % email.strip().lower())
                total_results += result
            message = f"{len(total_results.created)} users have been created," \
                      f"{len(total_results.updated)} updated." \
                      f"{len(total_results.skipped)} invalid entries found."

            # post process form
            flash(message, 'success')
        except Exception as e:
            flash(str(e), 'error')

    @expose('/load')
    @has_access
    def load(self):
        # do something with param1
        # and return it
        self.update_redirect()
        return self.render_template('uniset/user/load.html')

    list = load


class UserProfileView(ModelView):
    datamodel = SQLAInterface(UserProfile)
    list_columns = ['user', 'uuid', ]


appbuilder.add_separator('Security')

appbuilder.add_view(LoadUserView,
                    "Load users",
                    icon="fa-cloud-download",
                    category="Security",
                    category_icon="fa-envelope")

appbuilder.add_view(UserProfileView,
                    "User profiles",
                    icon="fa-user-circle",
                    category="Security",
                    category_icon="fa-cloud-download-alt")
