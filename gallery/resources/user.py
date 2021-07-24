from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource
from gallery.domain import create_user, login
from gallery.exceptions import UserAlreadyExists
from gallery.resources.schemas import LoginSchema, UserSchema
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
        except UserAlreadyExists as ex:
            return ex.to_dict(), ex.status_code
