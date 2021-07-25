from flask import Blueprint
from flask_restful import Api
from .user import GaleryResource, LoginResource, UserResource


bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)
api.add_resource(LoginResource, "/login")
api.add_resource(UserResource, "/users")
api.add_resource(GaleryResource, "/users/<string:user_id>/gallery")


def init_app(app):
    app.register_blueprint(bp)
