import sys
import warnings
from urllib.parse import unquote

import click
from colorama import Fore, Style

from flask import url_for
from flask.cli import FlaskGroup
from superset.cli import app, create_app

import uniset

warnings.simplefilter("ignore", UserWarning, 144)  # isort:skip


@app.cli.command()
@click.option('--verbose', '-v', is_flag=True, help='Show extra information')
def version(verbose):
    from uniset.app import app
    from superset import db

    line = Fore.BLUE + '-=' * 20

    config = app.config

    print(line)
    print('{y}UNIset {c}{univer}{w} based on {y}Superset {c}{version}'.format(
        w=Fore.WHITE,
        y=Fore.YELLOW,
        c=Fore.CYAN,
        univer=uniset.VERSION,
        version=config.get('VERSION_STRING')))
    print(line)
    if verbose:
        print('[DB] : ' + '{}'.format(db.engine))
    print(Style.RESET_ALL)


@app.cli.command()
@click.pass_context
def check(ctx):
    ctx.invoke(version, verbose=False)
    try:
        import superset_config  # noqa

        from superset import app
        assert app.config
        assert app.config.get('APP_NAME') == 'uniset'
        assert app.config.get('AUTH_TYPE') == 4
        print("Uniset configuration...OK")
    except Exception:
        print("Unable to load uniset configuration")
        sys.exit(1)

    try:
        from superset import appbuilder
        assert appbuilder.sm.auth_user_oauth.patched
        print("SecurityManager patch...OK")
    except (AssertionError, AttributeError):
        print("SecurityManager not patched")
        sys.exit(1)
    try:
        from flask_appbuilder import base
        assert base.dynamic_class_import.patched
        print("dynamic_class_import patch...OK")
    except (AssertionError, AttributeError):
        print("flask_appbuilder.base.dynamic_class_import not patched")
        sys.exit(1)


@app.cli.command()
@click.option('--short', '-s', is_flag=True, help='shorten output')
def list_routes(short):
    from uniset.app import app
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)
        if short:
            methods = ''
        else:
            methods = "{:25s}".format(','.join(rule.methods))

        url = url_for(rule.endpoint, **options)
        line = unquote("{:50s} {} {}".format(rule.endpoint, methods, url))
        output.append(line)
        print(line)

    for line in sorted(output):
        print(line)


@click.group(cls=FlaskGroup, create_app=create_app)
def main():
    """This is a management script for the uniset application."""


if __name__ == '__main__':
    main()
