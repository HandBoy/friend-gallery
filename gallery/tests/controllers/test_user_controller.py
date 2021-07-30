from gallery.documents import UserModel
from gallery.controllers.user_controller import create_user, find_user, login
from gallery.exceptions import UserAlreadyExists, UserNotFound
from mongoengine.errors import NotUniqueError
from pytest import raises


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


def test_fail_create_user_already_exists(mocker):
    # GIVE
    mocker.patch(
        "gallery.controllers.gallery_controller.UserModel.save",
        side_effect=NotUniqueError("vish"),
    )
    # Act
    # Assert
    with raises(UserAlreadyExists):
        create_user("email", "email@email", "123123")


def test_success_find_user(mocker):
    # GIVE
    mocker.patch(
        "gallery.controllers.gallery_controller.UserModel.find_by_id",
        return_value=UserModel(),
    )
    # Act

    # Assert
    user = find_user("123")
    assert user


def test_fail_find_user_and_user_not_found(mocker):
    # GIVE
    mocker.patch(
        "gallery.controllers.gallery_controller.UserModel.find_by_id",
        return_value=None,
    )
    # Act

    # Assert
    with raises(UserNotFound):
        find_user("1234")
