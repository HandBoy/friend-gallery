import uuid
from datetime import datetime

from flask_mongoengine import Document
from mongoengine import (
    DateTimeField,
    DoesNotExist,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    IntField,
    ObjectIdField,
    ReferenceField,
    StringField,
)
from mongoengine.errors import ValidationError
from mongoengine.fields import UUIDField

from gallery.ext.auth import pwd_context


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

    @staticmethod
    def encrypt_password(password):
        return pwd_context.encrypt(password)

    def check_encrypted_password(self, password):
        return pwd_context.verify(password, self.password)

    def to_dict(self):
        return {"email": self.email, "username": self.username}


class PicturesModel(EmbeddedDocument):
    id = UUIDField(default=str(uuid.uuid4()))
    slug = StringField(
        max_length=120,
        required=True,
    )
    name = StringField(
        max_length=120,
        required=True,
    )
    description = StringField(
        max_length=120,
        required=True,
    )
    url = StringField(
        max_length=120,
        required=True,
    )
    likes = IntField(default=0)
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField(default=datetime.utcnow())


class GaleryModel(Document):
    _id = ObjectIdField(required=False)
    name = StringField(max_length=120, required=True)
    user = ReferenceField(UserModel)
    pictures = EmbeddedDocumentListField(PicturesModel)
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField(default=datetime.utcnow())
