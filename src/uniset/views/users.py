from flask_appbuilder import ModelView, SimpleFormView, expose, has_access
from flask_appbuilder.fieldwidgets import (BS3TextAreaFieldWidget,
                                           Select2AJAXWidget,)
from flask_appbuilder.forms import DynamicForm
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.security.sqla.models import Role
from flask_babel import lazy_gettext as _
from wtforms import StringField, validators

from flask import flash
from superset import db

from uniset.models import UserProfile


class LoadUserForm(DynamicForm):
    emails = StringField('Emails',
                         description=_('Enter comma separated list of partial emails/usernames'),
                         validators=[validators.DataRequired()],
                         widget=BS3TextAreaFieldWidget())

    role = StringField('Role',
                       description=_('Select role users will belong to'),
                       validators=[validators.DataRequired()],
                       widget=Select2AJAXWidget(endpoint='/roles/api/readvalues'))


class LoadUserView(SimpleFormView):
    route_base = "/users2"
    form = LoadUserForm

    def form_post(self, form):
        from uniset.azure.synchronizer import SyncResult
        from uniset.synchronizer import UnisetSynchronizer

        try:
            synchronizer = UnisetSynchronizer()
            roles = SQLAInterface(Role, db.session)

            synchronizer.extra['role'] = roles.get(form.data['role'])
            emails = form.data['emails'].split(',')
            total_results = SyncResult()
            for email in emails:
                result = synchronizer.fetch_users("startswith(mail,'%s')" % email.strip().lower())
                total_results += result
            if not (total_results.created + total_results.updated):
                flash("No users found", 'warning')
            else:
                message = ("{} users have been created,"
                           "{} updated.").format(len(total_results.created),
                                                 len(total_results.updated))

                # post process form
                flash(message, 'success')
        except Exception as e:
            flash(str(e), 'error')

    @expose('/load')
    @has_access
    def load(self):
        self.update_redirect()
        return self.render_template('uniset/user/load.html')

    list = load


class UserProfileView(ModelView):
    datamodel = SQLAInterface(UserProfile)
    list_columns = ['user', 'uuid', ]
