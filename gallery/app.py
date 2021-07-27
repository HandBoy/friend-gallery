from flask import Flask
from gallery.ext import configuration, database, auth, serializer, s3
from gallery import resources
from gallery import exceptions


def create_app():
    app = Flask(__name__)
    configuration.init_app(app)
    database.init_app(app)
    auth.init_app(app)
    serializer.init_app(app)
    resources.init_app(app)
    s3.init_app(app)
    exceptions.handle_api_exceptions(app)

    return app
