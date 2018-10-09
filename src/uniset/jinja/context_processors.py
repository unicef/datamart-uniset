from flask import g
from superset import app


@app.context_processor
def chpro_roles():
    try:
        roles = [i.name for i in g.user.roles]
    except AttributeError:
        return {}
    return dict(user=g.user,
                is_admin='Admin' in roles,
                is_editor='Editor' in roles,
                is_viewer='Viewer' in roles)


@app.context_processor
def version():
    try:
        from superset import appbuilder, app, db, MyIndexView
        config = app.config
        from uniset import VERSION
        ss_version = config.get('VERSION_STRING')

        return dict(verion_uniset=VERSION,
                    verion_superset=ss_version,
                    version_label=f'uniset {VERSION} based on SuperSet {ss_version}')
    except AttributeError:
        return {}
