from flask import Blueprint
from flask_restful import Api
from .user import LoginResource


bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)
api.add_resource(LoginResource, "/login")


def init_app(app):
    app.register_blueprint(bp)
