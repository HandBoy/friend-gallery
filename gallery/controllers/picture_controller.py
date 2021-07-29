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
