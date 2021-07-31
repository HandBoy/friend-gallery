from gallery.controllers.gallery_controller import create_picture
from gallery.exceptions import GalleryPermission
from pytest import raises


def test_fail_you_dont_have_permission_for_upload(mocker, app, user):
    mocker.patch(
        (
            "gallery.controllers.gallery_controller"
            ".GalleryModel.find_gallery_by_id"
        ),
        return_value=user["gallery"],
    )
    mocker.patch(
        (
            "gallery.controllers.gallery_controller."
            "GalleryModel.do_you_have_permission_to_upload"
        ),
        return_value=False,
    )

    with raises(GalleryPermission):
        create_picture("123", "123", {})


def test_success_add_gallery_friend():
    pass
