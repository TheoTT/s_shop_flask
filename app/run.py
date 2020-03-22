import importlib
import logging

from flask import Flask, request
from flask.helpers import get_env
from flask_cors import CORS

from hobbit_core.err_handler import ErrHandler

from app.exts import db, migrate, ma, hobbit, cors, jwt
#from app.cmds import cmd_list


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    hobbit.init_app(app, db)
    cors.init_app(app)
    jwt.init_app(app)


def register_blueprints(app):
    from app import views
    for name in views.__all__:
        bp = getattr(importlib.import_module(f'app.views.{name}'), 'bp', None)
        if bp is not None:
            app.register_blueprint(bp, url_prefix='/api')


def register_error_handler(app):
    app.register_error_handler(Exception, ErrHandler.handler)


def register_cmds(app):
    for cmd in cmd_list:
        app.cli.add_command(cmd)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('app.configs.{}'.format(get_env()))
    # cors = CORS(app, resources=r"/*", origins=r"*", )

    with app.app_context():
        register_extensions(app)
        register_blueprints(app)
        # register_cmds(app)
    register_error_handler(app)

    @app.before_request
    def log_request_info():
        logger = logging.getLogger('werkzeug')
        if request.method in ['POST', 'PUT']:
            logger.info('Body: %s', request.get_data())

    return app


app = create_app()
