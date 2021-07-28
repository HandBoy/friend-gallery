from os import environ
from flask import Flask
from gallery.ext import database, auth, serializer, s3
from gallery import resources
from gallery import exceptions
from gallery.config import config_by_name


def create_app(config_name=None):
    app = Flask(__name__)

    # load object-based default configuration
    env = environ.get("FLASK_ENV", config_name)
    app.config.from_object(config_by_name[env])

    database.init_app(app)
    auth.init_app(app)
    serializer.init_app(app)
    resources.init_app(app)
    s3.init_app(app)
    exceptions.handle_api_exceptions(app)

    return app
