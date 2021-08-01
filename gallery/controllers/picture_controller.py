from mongoengine.errors import DoesNotExist

from gallery.documents import GalleryModel
from gallery.exceptions import (
    GalleryNotFound,
    GalleryPermission,
    PictureNotFound,
)


def get_pictures(user_id: str, gallery_id: str, page: int = 0, limit: int = 5):
    try:
        gallery = GalleryModel.find_gallery_by_id(id=gallery_id)

        if not gallery:
            raise GalleryNotFound(message="Gallery Not Found")

        if gallery.are_you_owner(user_id):
            return gallery.get_pictures(page, limit)

        return gallery.get_approved_pictures(page, limit)
    except DoesNotExist:
        raise GalleryNotFound(message="Gallery Not Found")


def count_pictures(gallery_id: str):
    return GalleryModel.objects(_id=gallery_id).get().pictures.count()


def like_picture(gallery_id: str, picture_id: str):
    gallery = GalleryModel.find_gallery_by_id(id=gallery_id)

    if not gallery:
        raise GalleryNotFound(message="Gallery Not Found")

    picture = gallery.pictures.filter(id=picture_id)
    try:
        picture.get().likes += 1
        picture.save()

        return True
    except DoesNotExist:
        raise PictureNotFound("Picture not Found")


def approve_picture(user_id: str, gallery_id: str, picture_id: str):
    gallery = GalleryModel.find_gallery_by_id(id=gallery_id)

    if not gallery:
        raise GalleryNotFound(message="Gallery Not Found")

    if not gallery.are_you_approver(user_id):
        raise GalleryPermission(
            message="You don't have permission for approve this picture"
        )

    picture = gallery.pictures.filter(id=picture_id)
    try:
        picture.get().approved = True
        picture.save()

        return True
    except DoesNotExist:
        raise PictureNotFound("Picture not Found")
