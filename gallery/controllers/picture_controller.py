from mongoengine.errors import DoesNotExist

from gallery.documents import GalleryModel
from gallery.exceptions import GalleryNotFound, GalleryPermission


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
    if GalleryModel.approve_picture(gallery_id, user_id, picture_id):
        return True

    raise GalleryPermission(
        message="You don't have permission for approve this picture"
    )
