from gallery.documents import UserModel
from gallery.domain import login


def test_fail_user_doesnot_exists(mocker):
    # GIVE
    mocker.patch("gallery.domain.UserModel.find_by_email", return_value=None)
    has_user = login("email@email", "123123")

    assert not has_user


def test_success_user_exists(mocker):
    # GIVE
    mocker.patch("gallery.domain.UserModel.find_by_email", return_value=UserModel())
    mocker.patch("gallery.domain.UserModel.check_encrypted_password", return_value=True)

    has_user = login("emailTrue@email", "123123")

    assert has_user
