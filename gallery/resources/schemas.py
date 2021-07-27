from gallery.ext.s3 import allowed_images_to_upload
from marshmallow import Schema, ValidationError, fields, validate, validates


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))


class EmailSchema(Schema):
    email = fields.Email(required=True)


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


class PictureSchema(Schema):
    id = fields.Str()
    name = fields.Str(required=True)
    url = fields.URL()
    description = fields.Str()
    likes = fields.Int(default=0)
    approved = fields.Bool(default=False)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class UploadPictureSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str()
    photo_file = fields.Raw(required=True, type="file")

    @validates("photo_file")
    def validate_photo_file(self, photo_file):
        if photo_file.filename == "":
            raise ValidationError("File without name.")
        if not allowed_images_to_upload(photo_file.filename):
            raise ValidationError("File type not accept.")
