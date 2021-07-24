from gallery.documents import UserModel


def login(email: str, password: str):
    user = UserModel.find_by_email(identity=email)

    if user and user.check_encrypted_password(password):
        return True

    return False
