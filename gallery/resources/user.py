from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource
from gallery.domain import login
from gallery.resources.schemas import LoginSchema
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
