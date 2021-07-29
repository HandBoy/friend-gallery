from mongoengine.errors import DoesNotExist, NotUniqueError
from werkzeug.utils import secure_filename

from gallery.documents import GalleryModel, PicturesModel, UserModel
from gallery.exceptions import (
    GalleryNotFound,
    GalleryPermission,
    UserAlreadyExists,
    UserNotFound,
)
from gallery.ext.auth import check_encrypted_password, encrypt_password
from gallery.ext.s3 import upload_file_to_s3


def login(email: str, password: str):
    user = UserModel.find_by_email(email=email)

    if user and check_encrypted_password(user.password, password):
        return user

    return None


def create_user(name: str, email: str, password: str):
    user = UserModel(
        name=name,
        email=email,
        password=encrypt_password(password),
    )

    try:
        user.validate()
        user.save()
        return user
    except NotUniqueError:
        raise UserAlreadyExists(message="User Already Exists")


def find_user(user_id: str):
    user = UserModel.find_by_id(user_id)
    if not user:
        raise UserNotFound(message="User Not Found")

    return user


def create_gallery(user: UserModel, raw_gallery: dict):
    # TODO Improve that
    gallery = GalleryModel(**raw_gallery)
    user.save()
    gallery.user = user.to_dbref()
    gallery.can_approve.append(user.to_dbref())
    gallery.save()


def get_user_galleries(user_id: str):
    galleries = GalleryModel.find_gallery_by_user(user_id=user_id)
    return galleries


def get_paginate_pictures(
    user_id: str, gallery_id: str, page: int = 0, limit: int = 5
):
    try:
        if GalleryModel.are_you_owner(gallery_id, user_id):
            return GalleryModel.get_pictures(gallery_id, page, limit)

        return GalleryModel.get_pictures_approved(gallery_id, page, limit)
    except DoesNotExist:
        raise GalleryNotFound(message="Gallery Not Found")


def count_pictures(gallery_id: str):
    return GalleryModel.objects(_id=gallery_id).get().pictures.count()


def get_gallery_by_user_and_id(user_id: str, gallery_id: str):
    gallery = GalleryModel.find_gallery_by_user_and_id(
        user_id=user_id, gallery_id=gallery_id
    )

    if not gallery:
        raise GalleryNotFound(message="Gallery Not Found")

    return gallery


def can_permission_to_upload_in_gallery(user_id, gallery_id):
    # gallery is your?
    gallery = GalleryModel.find_gallery_by_user_and_id(user_id, gallery_id)
    if not gallery:
        # your are friend ?
        gallery = GalleryModel.are_you_friend(user_id, gallery_id)
        if not gallery:
            return False

    return True


def create_picture(user_id: str, gallery_id: str, raw_picture: dict):
    if not can_permission_to_upload_in_gallery(user_id, gallery_id):
        raise GalleryPermission(message="You dont have permission for upload.")

    raw_picture["photo_file"].filename = (
        f"{user_id}/{gallery_id}/"
        f"{secure_filename(raw_picture['photo_file'].filename)}"
    )

    output = upload_file_to_s3(raw_picture["photo_file"])
    gallery = GalleryModel.find_gallery_by_id(gallery_id)

    picture = PicturesModel(
        name=raw_picture["name"],
        description=raw_picture["description"],
        url=str(output),
    )
    gallery.pictures.append(picture)
    gallery.save()

    return None, 201


def like_picture(gallery_id: str, picture_id: str):

    was_liked = GalleryModel.like_picture_by_id(
        gallery_id=gallery_id, picture_id=picture_id
    )

    if not was_liked:
        raise GalleryNotFound(message="Picture Not Found")

    return was_liked


def add_permission_to_approve(user_id: str, gallery_id: str, email: str):
    gallery = get_gallery_by_user_and_id(
        user_id=user_id, gallery_id=gallery_id
    )

    user = UserModel.find_by_email(email=email)
    if not user:
        raise UserNotFound(message="User Not Found")

    gallery.append_approver(user._id)


def approve_picture(user_id: str, gallery_id: str, picture_id: str):
    if GalleryModel.approve_picture(gallery_id, user_id, picture_id):
        return True

    raise GalleryPermission(
        message="You don't have permission for approve this picture"
    )


def add_gallery_friend(user_id: str, gallery_id: str, email: str):
    gallery = get_gallery_by_user_and_id(
        user_id=user_id, gallery_id=gallery_id
    )

    user = UserModel.find_by_email(email=email)
    if not user:
        raise UserNotFound(message="User Not Found")

    gallery.add_friend_to_upload(user._id)


class Paginator:
    def __init__(self, page, limit, url):
        self.page = self.validate(page, "page")
        self.limit = self.validate(limit, "limit")
        self.url = url

    @property
    def next_num(self):
        return self.page + 1

    @property
    def prev_num(self):
        return 0 if self.page == 0 else self.page - 1

    @property
    def next_page(self):
        return f"{self.url}?page={self.next_num}&limit={self.limit}"

    @property
    def previous_page(self):
        return f"{self.url}?page={self.prev_num}&limit={self.limit}"

    def validate(self, value, name):
        try:
            value = int(value)
            value = 0 if value < 0 else value
            return value
        except ValueError:
            raise Exception(message=f"Url Arg: {name}, must be integer")
