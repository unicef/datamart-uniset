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
@click.option('--short', '-s', is_flag=True, help='shorten output')
def list_routes(short):
    # class ListRoutes(Command):
    #     option_list = [Option('-s', '--short', action='store_true', help='shorten output')]
    #
    #     def run(self, short):
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


#
# def main():
#     from superset.cli import manager
#     from uniset.app import app  # noqa - Load uniset extras
#     manager.add_command('list_routes', ListRoutes())
#
#     manager.run()


@click.group(cls=FlaskGroup, create_app=create_app)
def main():
    """This is a management script for the uniset application."""


if __name__ == '__main__':
    main()
