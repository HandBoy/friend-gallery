from mongoengine.errors import NotUniqueError

from gallery.documents import GalleryModel, PicturesModel, UserModel
from gallery.exceptions import GalleryNotFound, UserAlreadyExists, UserNotFound


def login(email: str, password: str):
    user = UserModel.find_by_email(email=email)

    if user and user.check_encrypted_password(password):
        return True

    return False


def create_user(name: str, email: str, password: str):
    user = UserModel(
        name=name,
        email=email,
        password=UserModel.encrypt_password(password),
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
    gallery = GalleryModel(**raw_gallery)
    user.save()
    gallery.user = user.to_dbref()
    gallery.can_approve.append(user.to_dbref())
    gallery.save()


def get_user_galleries(user_id: str):
    galleries = GalleryModel.find_gallery_by_user(user_id=user_id)
    return galleries


def get_gallery_by_user_and_id(user_id: str, gallery_id: str):
    gallery = GalleryModel.find_gallery_by_user_and_id(
        user_id=user_id, gallery_id=gallery_id
    )

    if not gallery:
        raise GalleryNotFound(message="Gallery Not Found")

    return gallery


def get_pictures_by_user_and_gallery(user_id: str, gallery_id: str):
    gallery = get_gallery_by_user_and_id(
        user_id=user_id, gallery_id=gallery_id
    )

    return gallery.pictures


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
