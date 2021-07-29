from gallery.ext.s3 import allowed_images_to_upload
from marshmallow import Schema, ValidationError, fields, validate, validates


class EmailRequestSchema(Schema):
    email = fields.Email(required=True)


class LoginRequestSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class UserRequestSchema(Schema):
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))


class GalleryRequestSchema(Schema):
    name = fields.Str(required=True)


class PictureRequestSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str()
    photo_file = fields.Raw(required=True, type="file")

    @validates("photo_file")
    def validate_photo_file(self, photo_file):
        if photo_file.filename == "":
            raise ValidationError("File without name.")
        if not allowed_images_to_upload(photo_file.filename):
            raise ValidationError("File type not accept.")
