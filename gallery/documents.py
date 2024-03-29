from __future__ import annotations
from typing import List, Optional

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
    def find_galleries_by_user(user_id) -> List[GalleryModel]:
        try:
            galleries = list(GalleryModel.objects(user=user_id))
            return galleries
        except ValidationError:
            return []

    @staticmethod
    def find_gallery_by_id(id) -> Optional[GalleryModel]:
        try:
            gallery = GalleryModel.objects(_id=id).get()
            return gallery
        except (DoesNotExist, ValidationError):
            return None

    @staticmethod
    def find_gallery_by_user_and_id(
        user_id, gallery_id
    ) -> Optional[GalleryModel]:
        try:
            gallery = GalleryModel.objects(user=user_id, _id=gallery_id).get()
            return gallery
        except (DoesNotExist, ValidationError):
            return None

    def get_pictures(self, page=0, limit=5) -> PicturesModel:
        first = page * limit

        paginated_pics = (
            GalleryModel.objects(_id=self._id)
            .fields(slice__pictures=[first, limit])
            .get()
            .pictures
        )

        return paginated_pics

    def get_approved_pictures(self, page=0, limit=5) -> PicturesModel:
        paginated_pics = self.get_pictures(page, limit).filter(approved=True)

        return paginated_pics

    def do_you_have_permission_to_upload(self, user_id) -> bool:
        if not self.are_you_owner(user_id):
            if not self.are_you_friend(user_id):
                return False

        return True

    def are_you_owner(self, user_id: str) -> bool:
        if str(user_id) == str(self.user._id):
            return True

        return False

    def are_you_friend(self, user_id) -> bool:
        for user in self.friends:
            if user_id == str(user.id):
                return True

        return False

    def are_you_approver(self, user_id) -> bool:
        for user in self.can_approve:
            if user_id == user.id:
                return True

        return False

    def append_approver(self, user_id):
        self.can_approve.append(user_id)
        self.save()

    def add_friend_to_upload(self, user_id):
        self.friends.append(user_id)
        self.save()
