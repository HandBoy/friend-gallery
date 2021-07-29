from marshmallow import Schema, fields


class LoginResponseSchema(Schema):
    access_token = fields.Str(required=True)
    refresh_token = fields.Str(required=True)


class GalleryResponseSchema(Schema):
    id = fields.Str(attribute="_id")
    name = fields.Str(required=True)
    created_at = fields.DateTime()


class PictureResponseSchema(Schema):
    id = fields.Str()
    name = fields.Str(required=True)
    url = fields.URL()
    description = fields.Str()
    likes = fields.Int(dump_default=0)
    approved = fields.Bool(dump_default=False)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class PicturePagResponseSchema(Schema):
    count = fields.Int()
    next_page = fields.Str()
    previous_page = fields.Str()
    result = fields.Nested(PictureResponseSchema, many=True)
