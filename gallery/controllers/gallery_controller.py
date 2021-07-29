from gallery.documents import GalleryModel, PicturesModel, UserModel
from gallery.exceptions import GalleryNotFound, GalleryPermission, UserNotFound
from gallery.ext.s3 import upload_file_to_s3
from werkzeug.utils import secure_filename


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
