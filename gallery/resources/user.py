from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
)
from flask_restful import Resource
from gallery.domain import (
    create_gallery,
    create_picture,
    create_user,
    find_user,
    get_user_galleries,
    get_pictures_by_user_and_gallery,
    login,
)
from gallery.exceptions import GalleryNotFound, UserAlreadyExists, UserNotFound
from gallery.resources.schemas import (
    GalerySchema,
    LoginSchema,
    PictureSchema,
    UserSchema,
)
from marshmallow.exceptions import ValidationError


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        try:
            data = LoginSchema().load(request.get_json())

            if login(**data):
                access_token = create_access_token(identity=data["email"])
                refresh_token = create_refresh_token(identity=data["email"])

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
        galery = get_user_galleries(user_id)
        return GalerySchema(many=True).dump(galery), 200


class PicturesResource(Resource):
    @jwt_required()
    def get(self, user_id, gallery_id):
        try:
            pictures = get_pictures_by_user_and_gallery(user_id, gallery_id)
            return PictureSchema(many=True).dump(pictures), 200
        except GalleryNotFound as err:
            return err.to_dict(), err.status_code

    @jwt_required()
    def post(self, user_id, gallery_id):
        try:
            picture = PictureSchema().load(request.get_json())

            create_picture(
                user_id=user_id, gallery_id=gallery_id, raw_picture=picture
            )
            return None, 201

        except ValidationError as err:
            return err.messages, 422
        except GalleryNotFound as err:
            return err.to_dict(), err.status_code
