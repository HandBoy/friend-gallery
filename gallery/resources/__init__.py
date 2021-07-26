from flask import Blueprint
from flask_restful import Api
from .user import (
    UserGalleriesResource,
    LoginResource,
    PicturesResource,
    UserResource,
    PicturesApproveResource,
    PictureLikeResource,
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
api.add_resource(
    PictureLikeResource,
    "/gallery/<string:gallery_id>/pictures/<string:picture_id>/like",
)
api.add_resource(
    PicturesApproveResource,
    "/gallery/<string:gallery_id>/approver",
)


def init_app(app):
    app.register_blueprint(bp)
