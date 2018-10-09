from six import text_type

import sqlalchemy
from flask_appbuilder import SimpleFormView
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect, secure_filename

from flask import abort, flash, g
from superset import app, appbuilder

from superset_config import SQLALCHEMY_DATABASE_URI

from ..forms.databases import LoadSQLForm

config = app.config


# simple_page = Blueprint('simple_page', __name__, template_folder='templates')
#
#
# @simple_page.route('/', defaults={'page': 'index'})
# @simple_page.route('/<page>')
# def show(page):
#     return "Ok"
#
#
# app.register_blueprint(simple_page)


class LoadSQL(SimpleFormView):
    form = LoadSQLForm
    form_title = _('Database creation')
    add_columns = ['database', 'schema', 'table_name']

    def form_get(self, form):
        # Explicitly checking "Admin" permissions
        if 'Admin' not in [i.name for i in g.user.roles]:
            abort(401)

    def form_post(self, form):
        # Explicitly checking "Admin" permissions
        if 'Admin' not in [i.name for i in g.user.roles]:
            abort(401)

        # Note: This is intrinsically insecure.
        # Anyone with access to this view can execute custom commands on the DB.

        sql_file = form.sql_file.data
        form.sql_file.data.filename = secure_filename(form.sql_file.data.filename)
        sql_filename = form.sql_file.data.filename
        try:
            engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI)
            conn = engine.raw_connection()
            with conn.cursor() as cursor:
                cursor.execute(f"create database {form.db_name.data}")
                cursor.execute(f"use {form.db_name.data}")
                contents = sql_file.stream.read()
                commands = contents.decode().split(';\n')
                for command in commands:
                    if command.rstrip() != '':
                        cursor.execute(command)
            conn.commit()
            conn.close()
        except Exception as e:
            message = text_type(e)
            flash(
                message,
                'danger')
            return redirect('/loadsql/form')

        # Go back to welcome page / splash screen
        message = _(f'SQL file "{sql_filename}" uploaded database "{form.db_name.data}"')
        flash(message, 'info')
        return redirect('/tablemodelview/list/')


appbuilder.add_view(LoadSQL, 'LoadSQL',
                    category='Sources',
                    icon='fa-upload', )

# Reorganize Sources.
# Move UploadCSV to the end
menu = appbuilder.menu.menu[2]
i = [x.name for x in menu.childs].index('Upload a CSV')
csv = appbuilder.menu.menu[2].childs.pop(i)
appbuilder.menu.menu[2].childs.append(csv)
# Remove double hyphen
for i in range(1, len(menu.childs)):
    if menu.childs[i - 1].name == '-' and menu.childs[i].name == '-':
        menu.childs.pop(i - 1)
        menu.childs.pop(i - 1)
        break
# Change table icon
i = [x.name for x in menu.childs].index('Tables')
appbuilder.menu.menu[2].childs[i].icon = 'fa-table'
