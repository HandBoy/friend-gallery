from gallery.controllers.user_controller import find_user
from gallery.documents import GalleryModel, PicturesModel, UserModel
from gallery.exceptions import GalleryNotFound, GalleryPermission, UserNotFound
from gallery.ext.s3 import upload_file_to_s3


def create_gallery(user: UserModel, raw_gallery: dict):
    gallery = GalleryModel(**raw_gallery)
    gallery.user = user._id
    gallery.can_approve.append(user._id)
    gallery.save()


def get_user_galleries(user_id: str):
    find_user(user_id)
    galleries = GalleryModel.find_galleries_by_user(user_id=user_id)
    return galleries


def get_gallery_by_user_and_id(user_id: str, gallery_id: str):
    gallery = GalleryModel.find_gallery_by_user_and_id(
        user_id=user_id, gallery_id=gallery_id
    )

    if not gallery:
        raise GalleryNotFound(message="Gallery Not Found")

    return gallery


def create_picture(user_id: str, gallery_id: str, raw_picture: dict):
    gallery = GalleryModel.find_gallery_by_id(id=gallery_id)

    if not gallery:
        raise GalleryNotFound(message="Gallery Not Found")

    if not gallery.do_you_have_permission_to_upload(user_id):
        raise GalleryPermission(message="You dont have permission to upload.")

    output = upload_file_to_s3(raw_picture["photo_file"])

    picture = PicturesModel(
        name=raw_picture["name"],
        description=raw_picture["description"],
        url=str(output),
    )
    gallery.pictures.append(picture)
    gallery.cascade_save()

    return None, 201


def add_permission_to_approve(user_id: str, gallery_id: str, email: str):
    gallery = get_gallery_by_user_and_id(
        user_id=user_id, gallery_id=gallery_id
    )

    user = UserModel.find_by_email(email=email)
    if not user:
        raise UserNotFound(message="User Not Found")

    gallery.append_approver(user._id)


def add_gallery_friend(user_id: str, gallery_id: str, email: str):
    gallery = get_gallery_by_user_and_id(
        user_id=user_id, gallery_id=gallery_id
    )

    user = UserModel.find_by_email(email=email)
    if not user:
        raise UserNotFound(message="User Not Found")

    gallery.add_friend_to_upload(user._id)
