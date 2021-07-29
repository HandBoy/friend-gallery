from gallery.controllers.user_controller import create_user, login
from gallery.documents import UserModel


def test_fail_user_doesnot_exists(mocker):
    # Give
    mocker.patch(
        "gallery.controllers.gallery_controller.UserModel.find_by_email",
        return_value=None,
    )
    # Act
    has_user = login("email@email", "123123")
    # Assert
    assert not has_user


def test_success_user_exists(mocker):
    # GIVE
    mocker.patch(
        "gallery.controllers.gallery_controller.UserModel.find_by_email",
        return_value=UserModel(),
    )
    mocker.patch(
        "gallery.controllers.user_controller.check_encrypted_password",
        return_value=True,
    )
    # Act
    has_user = login("emailTrue@email", "123123")
    # Assert
    assert has_user


def test_success_create_user(mocker):
    # GIVE
    mocker.patch(
        "gallery.controllers.gallery_controller.UserModel.save",
        return_value=True,
    )
    # Act
    has_user = create_user("email", "email@email", "123123")
    # Assert
    assert has_user
