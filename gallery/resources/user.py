from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_jwt,
    jwt_required,
)
from flask_restful import Resource
from gallery.domain import (
    add_permission_to_approve,
    approve_picture,
    create_gallery,
    create_picture,
    create_user,
    find_user,
    get_pictures,
    get_user_galleries,
    like_picture,
    login,
)
from gallery.exceptions import (
    GalleryNotFound,
    UserAlreadyExists,
    UserNotFound,
)
from gallery.resources.schemas import (
    EmailSchema,
    GalerySchema,
    LoginSchema,
    PictureSchema,
    UploadPictureSchema,
    UserSchema,
)
from marshmallow.exceptions import ValidationError


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        try:
            data = LoginSchema().load(request.get_json())
            user = login(**data)
            if user:
                info = {"email": user.email, "id": str(user._id)}
                access_token = create_access_token(info)
                refresh_token = create_refresh_token(info)

                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }, 200

        except ValidationError as err:
            return err.messages, 422

        return {"error": True, "message": "Wrong credentials"}, 401


class UserResource(Resource):
    def post(self):
        try:
            data = UserSchema().load(request.get_json())
            if create_user(**data):
                return {"message": "User added sucessfully"}, 201
        except ValidationError as err:
            return err.messages, 422
        except UserAlreadyExists as err:
            return err.to_dict(), err.status_code


class UserGalleriesResource(Resource):
    @jwt_required()
    def post(self, user_id):
        try:
            user = find_user(user_id)
            galery = GalerySchema().load(request.get_json())

            create_gallery(user=user, raw_gallery=galery)

            return {}, 201
        except ValidationError as err:
            return err.messages, 422
        except UserNotFound as err:
            return err.to_dict(), err.status_code

    @jwt_required()
    def get(self, user_id):
        print(get_jwt())

        galery = get_user_galleries(user_id)
        return GalerySchema(many=True).dump(galery), 200


class PicturesResource(Resource):
    @jwt_required()
    def get(self, gallery_id):
        try:
            current_user = get_current_user()
            pictures = get_pictures(current_user._id, gallery_id)
            return PictureSchema(many=True).dump(pictures), 200
        except GalleryNotFound as err:
            return err.to_dict(), err.status_code

    @jwt_required()
    def post(self, gallery_id):
        try:
            data = {**dict(request.files), **dict(request.form)}

            picture = UploadPictureSchema().load(data)

            current_user = get_current_user()

            create_picture(
                user_id=current_user._id,
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


class ApproverResource(Resource):
    @jwt_required()
    def post(self, gallery_id):
        try:
            current_user = get_current_user()
            schema = EmailSchema().load(request.get_json())
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
