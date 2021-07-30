from gallery.controllers.gallery_controller import (
    can_permission_to_upload_in_gallery, create_picture)
from gallery.exceptions import GalleryPermission
from pytest import raises


def test_fail_you_dont_have_permission_to_upload(mocker, app, user):
    mocker.patch(
        "gallery.controllers.gallery_controller.GalleryModel.find_gallery_by_user_and_id",
        return_value=False,
    )
    mocker.patch(
        "gallery.controllers.gallery_controller.GalleryModel.are_you_friend",
        return_value=False,
    )
    has_permission = can_permission_to_upload_in_gallery(user["user"]._id, 1)
    assert not has_permission


def test_fail_you_dont_have_permission_for_upload(mocker):
    mocker.patch(
        "gallery.controllers.gallery_controller.can_permission_to_upload_in_gallery",
        return_value=False,
    )

    with raises(GalleryPermission):
        create_picture("123", "123", {})


def test_success_add_gallery_friend()