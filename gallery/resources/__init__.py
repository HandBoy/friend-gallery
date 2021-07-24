from flask import Blueprint
from flask_restful import Api
from .user import LoginResource, UserResource


bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)
api.add_resource(LoginResource, "/login")
api.add_resource(UserResource, "/users")


def init_app(app):
    app.register_blueprint(bp)
