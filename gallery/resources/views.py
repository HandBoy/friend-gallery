from gallery.paginator import Paginator
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    jwt_required,
)
from flask_restful import Resource
from gallery.controllers.gallery_controller import (
    add_gallery_friend,
    add_permission_to_approve,
    create_gallery,
    create_picture,
    get_user_galleries,
)
from gallery.controllers.user_controller import create_user, login
from gallery.controllers.picture_controller import (
    approve_picture,
    count_pictures,
    get_paginate_pictures,
    like_picture,
)
from gallery.exceptions import (
    GalleryNotFound,
    LoginUnauthorized,
    UserAlreadyExists,
)
from gallery.resources.serializers.inbound import (
    EmailRequestSchema,
    GalleryRequestSchema,
    LoginRequestSchema,
    PictureRequestSchema,
    UserRequestSchema,
)
from gallery.resources.serializers.outbound import (
    GalleryResponseSchema,
    LoginResponseSchema,
    PicturePagResponseSchema,
)
from marshmallow.exceptions import ValidationError


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        try:
            data = LoginRequestSchema().load(request.get_json())
            user = login(**data)
            if user:
                info = {"email": user.email, "id": str(user._id)}
                data = LoginResponseSchema().dump(
                    {
                        "access_token": create_access_token(info),
                        "refresh_token": create_refresh_token(info),
                    }
                )

                return data, 200

        except ValidationError as err:
            return err.messages, 400

        raise LoginUnauthorized("Your login or password dont match")


class UserResource(Resource):
    def post(self):
        try:
            data = UserRequestSchema().load(request.get_json())
            if create_user(**data):
                return None, 201
        except ValidationError as err:
            return err.messages, 400
        except UserAlreadyExists as err:
            return err.to_dict(), err.status_code


class UserGalleriesResource(Resource):
    @jwt_required()
    def get(self, user_id):
        galery = get_user_galleries(user_id)
        return GalleryResponseSchema(many=True).dump(galery), 200


class GalleriesResource(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user = get_current_user()
            galery = GalleryRequestSchema().load(request.get_json())

            create_gallery(user=current_user, raw_gallery=galery)

            return None, 201
        except ValidationError as err:
            return err.messages, 400

    @jwt_required()
    def get(self):
        current_user = get_current_user()
        galery = get_user_galleries(current_user._id)
        return GalleryResponseSchema(many=True).dump(galery), 200


class PicturesResource(Resource):
    @jwt_required()
    def get(self, gallery_id):
        try:
            paginator = Paginator(
                page=request.args.get("page", 0),
                limit=request.args.get("limit", 5),
                url=f"/gallery/{gallery_id}/pictures",
            )

            current_user = get_current_user()

            pictures = get_paginate_pictures(
                current_user._id, gallery_id, paginator.page, paginator.limit
            )
            count = count_pictures(gallery_id)

            data = {
                "previous_page": paginator.previous_page,
                "next_page": paginator.next_page,
                "count": count,
                "result": pictures,
            }
            pag = PicturePagResponseSchema().dump(data)

            return pag, 200
        except GalleryNotFound as err:
            return err.to_dict(), err.status_code
        except ValidationError as err:
            return err.messages, 400

    @jwt_required()
    def post(self, gallery_id):
        try:
            data = {**dict(request.files), **dict(request.form)}

            picture = PictureRequestSchema().load(data)

            current_user = get_current_user()

            create_picture(
                user_id=str(current_user._id),
                gallery_id=gallery_id,
                raw_picture=picture,
            )
            return None, 201

        except ValidationError as err:
            return err.messages, 400
        except GalleryNotFound as err:
            return err.to_dict(), err.status_code


class PictureLikeResource(Resource):
    @jwt_required()
    def post(self, gallery_id, picture_id):
        try:
            like_picture(gallery_id=gallery_id, picture_id=picture_id)
            return None, 200

        except ValidationError as err:
            return err.messages, 422
        except GalleryNotFound as err:
            return err.to_dict(), err.status_code


class ApproverGalleryResource(Resource):
    @jwt_required()
    def post(self, gallery_id):
        try:
            current_user = get_current_user()
            schema = EmailRequestSchema().load(request.get_json())
            add_permission_to_approve(
                current_user._id, gallery_id, schema["email"]
            )
            return None, 200

        except ValidationError as err:
            return err.messages, 400


class ApprovePicturesResource(Resource):
    @jwt_required()
    def put(self, gallery_id, picture_id):
        try:
            current_user = get_current_user()
            approve_picture(current_user._id, gallery_id, picture_id)
            return None, 200

        except ValidationError as err:
            return err.messages, 400


class FriendGalleryResource(Resource):
    @jwt_required()
    def post(self, gallery_id):
        try:
            current_user = get_current_user()
            schema = EmailRequestSchema().load(request.get_json())
            add_gallery_friend(
                user_id=current_user._id,
                gallery_id=gallery_id,
                email=schema["email"],
            )
            return None, 200

        except ValidationError as err:
            return err.messages, 400
