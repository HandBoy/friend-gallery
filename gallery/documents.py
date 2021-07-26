import uuid
from datetime import datetime

from flask_mongoengine import Document
from mongoengine import (
    DateTimeField,
    DoesNotExist,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    IntField,
    ListField,
    ObjectIdField,
    ReferenceField,
    StringField,
)
from mongoengine.errors import ValidationError
from mongoengine.fields import BooleanField, UUIDField


class UserModel(Document):
    _id = ObjectIdField(required=False)
    email = StringField(max_length=120, required=True, unique=True)
    name = StringField(max_length=120, required=True)
    password = StringField(required=True)

    @staticmethod
    def find_by_email(email):
        try:
            current_user = UserModel.objects(email=email).get()
            return current_user
        except DoesNotExist:
            return None

    @staticmethod
    def find_by_id(user_id):
        try:
            current_user = UserModel.objects(_id=user_id).get()
            return current_user
        except (DoesNotExist, ValidationError):
            return None

    def to_dict(self):
        return {"email": self.email, "username": self.username}


class PicturesModel(EmbeddedDocument):
    id = UUIDField(default=str(uuid.uuid4()))
    name = StringField(
        max_length=120,
        required=True,
    )
    description = StringField(
        max_length=120,
        required=False,
    )
    url = StringField(
        max_length=120,
        required=True,
    )
    likes = IntField(default=0)
    approved = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField(default=datetime.utcnow())


class GalleryModel(Document):
    _id = ObjectIdField(required=False)
    name = StringField(max_length=120, required=True)
    user = ReferenceField(UserModel)
    can_approve = ListField(ReferenceField(UserModel))
    pictures = EmbeddedDocumentListField(PicturesModel)
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField(default=datetime.utcnow())

    @staticmethod
    def find_gallery_by_user(user_id):
        try:
            galleries = list(GalleryModel.objects(user=user_id))
            return galleries
        except ValidationError:
            return None

    @staticmethod
    def find_gallery_by_user_and_id(user_id, gallery_id):
        try:
            gallery = GalleryModel.objects(user=user_id, _id=gallery_id).get()
            return gallery
        except (DoesNotExist, ValidationError):
            return None

    @staticmethod
    def like_picture_by_id(gallery_id, picture_id):
        try:
            picture = (
                GalleryModel.objects(_id=gallery_id)
                .get()
                .pictures.filter(id=picture_id)
            )
            picture.get().likes += 1
            picture.save()
            return True
        except (DoesNotExist, ValidationError):
            return False

    def append_approver(self, user_id):
        try:
            self.can_approve.append(user_id)
            self.save()
            return True
        except (DoesNotExist, ValidationError):
            return False
