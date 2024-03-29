from flask import Blueprint
from flask_restful import Api
from .views import (
    ApprovePicturesResource,
    FriendGalleryResource,
    GalleriesResource,
    UserGalleriesResource,
    LoginResource,
    PicturesResource,
    UserResource,
    ApproverGalleryResource,
    PictureLikeResource,
)


def init_app(app):
    bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
    api = Api(bp)
    # User
    api.add_resource(LoginResource, "/login")
    api.add_resource(UserResource, "/users")
    api.add_resource(
        UserGalleriesResource, "/users/<string:user_id>/galleries"
    )
    # Galleries
    api.add_resource(GalleriesResource, "/galleries")

    api.add_resource(
        ApproverGalleryResource,
        "/gallery/<string:gallery_id>/approver",
    )
    api.add_resource(
        FriendGalleryResource,
        "/gallery/<string:gallery_id>/friend",
    )
    # Pictures
    api.add_resource(
        PicturesResource,
        "/gallery/<string:gallery_id>/pictures",
    )
    api.add_resource(
        PictureLikeResource,
        "/gallery/<string:gallery_id>/pictures/<string:picture_id>/like",
    )
    api.add_resource(
        ApprovePicturesResource,
        "/gallery/<string:gallery_id>/pictures/<string:picture_id>/approve",
    )
    app.register_blueprint(bp)
