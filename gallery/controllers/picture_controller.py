from mongoengine.errors import DoesNotExist

from gallery.documents import GalleryModel
from gallery.exceptions import (
    GalleryNotFound,
    GalleryPermission,
    PictureNotFound,
)


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


def like_picture(gallery_id: str, picture_id: str):

    was_liked = GalleryModel.like_picture_by_id(
        gallery_id=gallery_id, picture_id=picture_id
    )

    if not was_liked:
        raise GalleryNotFound(message="Picture Not Found")

    return was_liked


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
