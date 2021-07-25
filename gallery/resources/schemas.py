from marshmallow import Schema, fields, validate


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))


class UserSchema(Schema):
    id = fields.Str(attribute="_id")
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class GalerySchema(Schema):
    id = fields.Str(attribute="_id")
    name = fields.Str(required=True)
    created_at = fields.DateTime()
