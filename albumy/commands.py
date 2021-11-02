import click

from albumy.extensions import db
from albumy.models import Role


def register_commands(app):

    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    
    @app.cli.command()
    def init():
        click.echo('Initializing the database...')
        db.create_all()

        click.echo('Initailing the roles and permissions...')
        Role.init_role()

        click.echo('Done.')
