from flask import Flask
from gallery.ext import configuration, database, auth, serializer
from gallery import resources


def create_app():
    app = Flask(__name__)
    configuration.init_app(app)
    database.init_app(app)
    auth.init_app(app)
    serializer.init_app(app)
    resources.init_app(app)
    return app
