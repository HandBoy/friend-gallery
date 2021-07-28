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
    can_approve = ListField(ReferenceField(UserModel), default=[])
    friends = ListField(ReferenceField(UserModel), default=[])
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
    def find_gallery_by_id(id):
        try:
            gallery = GalleryModel.objects(_id=id).get()
            return gallery
        except (DoesNotExist, ValidationError):
            return None

    @staticmethod
    def find_gallery_by_user_and_id(user_id, gallery_id):
        try:
            gallery = GalleryModel.objects(user=user_id, _id=gallery_id).get()
            return gallery
        except (DoesNotExist, ValidationError):
            return None

    @staticmethod
    def get_pictures_by_user_and_gallery_id(user_id, gallery_id):
        gallery = GalleryModel.find_gallery_by_user_and_id(user_id, gallery_id)

        if not gallery:
            return None

        return gallery.pictures

    @staticmethod
    def get_pictures_approved(gallery_id):
        pictures = (
            GalleryModel.objects(_id=gallery_id)
            .get()
            .pictures.filter(approved=True)
        )

        return pictures

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

    @staticmethod
    def approve_picture(gallery_id, user_id, picture_id, status=True):
        can_approve = GalleryModel.objects(
            _id=gallery_id, can_approve__in=[user_id]
        )

        if not can_approve:
            return False

        picture = can_approve.get().pictures.filter(id=picture_id)
        picture.get().approved = status
        picture.save()

        return True

    @staticmethod
    def you_are_friend(user_id, gallery_id):
        if not GalleryModel.objects(_id=gallery_id, friends__in=[user_id]):
            return False

        return True

    def append_approver(self, user_id):
        self.can_approve.append(user_id)
        self.save()

    def add_friend_to_upload(self, user_id):
        self.friends.append(user_id)
        self.save()
