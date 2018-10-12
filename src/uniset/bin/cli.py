import warnings
from urllib.parse import unquote

from colorama import Fore, Style
from flask_script import Command, Option

from flask import url_for

import uniset

warnings.simplefilter("ignore", UserWarning, 144)  # isort:skip


class Version(Command):
    option_list = [Option('-v', '--verbose', action='store_true', help='Show extra information')]

    def run(self, verbose):
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


class ListRoutes(Command):
    option_list = [Option('-s', '--short', action='store_true', help='shorten output')]

    def run(self, short):
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


def main():
    from superset.cli import manager
    manager.add_command('list_routes', ListRoutes())

    manager.run()
