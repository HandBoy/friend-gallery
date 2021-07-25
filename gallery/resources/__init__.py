from flask import Blueprint
from flask_restful import Api
from .user import (
    UserGalleriesResource,
    LoginResource,
    PicturesResource,
    UserResource,
)


bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)
api.add_resource(LoginResource, "/login")
api.add_resource(UserResource, "/users")
api.add_resource(UserGalleriesResource, "/users/<string:user_id>/gallery")
api.add_resource(
    PicturesResource,
    "/users/<string:user_id>/gallery/<string:gallery_id>/pictures",
)


def init_app(app):
    app.register_blueprint(bp)
