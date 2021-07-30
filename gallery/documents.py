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
    def get_pictures(gallery_id, page=0, limit=5):
        first = page * limit

        paginated_pics = (
            GalleryModel.objects(_id=gallery_id)
            .fields(slice__pictures=[first, limit])
            .get()
            .pictures
        )

        return paginated_pics

    @staticmethod
    def get_pictures_approved(gallery_id, page=0, limit=10):
        paginated_pics = GalleryModel.get_pictures(
            gallery_id, page=0, limit=5
        ).filter(approved=True)

        return paginated_pics

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
    def are_you_friend(user_id, gallery_id):
        if not GalleryModel.objects(_id=gallery_id, friends__in=[user_id]):
            return False

        return True

    @staticmethod
    def are_you_owner(gallery_id, user_id):
        owner = GalleryModel.find_gallery_by_user_and_id(user_id, gallery_id)

        if not owner:
            return False

        return True

    def append_approver(self, user_id):
        self.can_approve.append(user_id)
        self.save()

    def add_friend_to_upload(self, user_id):
        self.friends.append(user_id)
        self.save()

    def are_you_approver(self, user_id):
        for user in self.can_approve:
            if user_id == user.id:
                return True

        return False
