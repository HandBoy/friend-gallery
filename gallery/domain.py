from gallery.ext.auth import encrypt_password, check_encrypted_password
from mongoengine.errors import NotUniqueError, DoesNotExist

from gallery.documents import GalleryModel, PicturesModel, UserModel
from gallery.exceptions import (
    GalleryNotFound,
    GalleryPermission,
    UserAlreadyExists,
    UserNotFound,
)


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


def get_pictures(user_id: str, gallery_id: str):
    try:
        pictures = GalleryModel.get_pictures_by_user_and_gallery_id(
            user_id=user_id, gallery_id=gallery_id
        )

        if pictures:
            return pictures

        return GalleryModel.get_pictures_approved(gallery_id=gallery_id)
    except DoesNotExist:
        raise GalleryNotFound(message="Gallery Not Found")


def get_gallery_by_user_and_id(user_id: str, gallery_id: str):
    gallery = GalleryModel.find_gallery_by_user_and_id(
        user_id=user_id, gallery_id=gallery_id
    )

    if not gallery:
        raise GalleryNotFound(message="Gallery Not Found")

    return gallery


def create_picture(user_id: str, gallery_id: str, raw_picture: dict):
    gallery = get_gallery_by_user_and_id(
        user_id=user_id, gallery_id=gallery_id
    )

    picture = PicturesModel(**raw_picture)
    gallery.pictures.append(picture)
    gallery.save()


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
        message="You dont have permission for approve this picture"
    )
