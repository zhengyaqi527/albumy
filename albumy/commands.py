import click

from albumy.extensions import db
from albumy.models import Role


def cli_commands(app):

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
    @click.option('--user', default=10, help='Quantity of users, default is 10.')
    @click.option('--photo', default=50, help='Quantity os photots, default is 50')
    def forge(user, photo):
        """Generate fake data."""

        from albumy.fakes import fake_admin, fake_photo, fake_user

        click.echo('Initializing the roles and permissions...')
        Role.init_role()
        click.echo('Generating the administrator...')
        fake_admin()
        click.echo('Generating %d users...' % user )
        fake_user(30)
        click.echo('Generating %d photos...' % photo)
        fake_photo(photo)
        click.echo('Done.')