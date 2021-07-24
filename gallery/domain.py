from gallery.exceptions import UserAlreadyExists
from gallery.documents import UserModel
from mongoengine.errors import NotUniqueError


def login(email: str, password: str):
    user = UserModel.find_by_email(identity=email)

    if user and user.check_encrypted_password(password):
        return True

    return False


def create_user(name, email, password):
    user = UserModel(
        name=name,
        email=email,
        password=UserModel.encrypt_password(password),
    )

    try:
        user.validate()
        user.save()
        return user
    except NotUniqueError:
        raise UserAlreadyExists(message="User Already Exists")
