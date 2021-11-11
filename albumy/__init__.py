import os

from flask import Flask, render_template

from albumy.blueprints.main import main_bp
from albumy.blueprints.auth import auth_bp
from albumy.blueprints.user import user_bp
from albumy.settings import config
from albumy.extensions import db, bootstrap, mail, login_manager, migrate, moment, dropzone, avatars
from albumy.models import User, Role, Permission
from albumy.commands import cli_commands


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'development')
    
    app = Flask('albumy')

    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_shell_context(app)
    register_template_context(app)
    register_errorhandlers(app)
    register_commands(app)
    register_commands(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    dropzone.init_app(app)
    avatars.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User, Role=Role, Permission=Permission)


def register_template_context(app):
    pass


def register_errorhandlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return render_template('errors/413.html'), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

def register_commands(app):
    cli_commands(app)
