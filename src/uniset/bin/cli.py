import os
import warnings

from colorama import Fore, Style
from flask_script import Command, Option

from flask import Blueprint, url_for
from superset import app, appbuilder, db
from superset.cli import manager

import uniset

warnings.simplefilter("ignore", UserWarning, 144)  # isort:skip


class Version(Command):
    option_list = [Option('-v', '--verbose', action='store_true', help='Show extra information')]

    def run(self, verbose):
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


@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)


def main():
    from uniset import ROOT

    app.jinja_loader.searchpath.insert(0, os.path.join(ROOT, 'templates'))

    bp = Blueprint('uniset', __name__, url_prefix='/static',
                   template_folder='templates',
                   static_folder=os.path.join(ROOT, 'static'),
                   static_url_path='/uniset')
    appbuilder.get_app.register_blueprint(bp)

    from uniset import views
    from uniset.jinja import context_processors  # noqa

    manager.run()
