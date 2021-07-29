from gallery.documents import UserModel
from gallery.exceptions import UserAlreadyExists, UserNotFound
from gallery.ext.auth import check_encrypted_password, encrypt_password
from mongoengine.errors import NotUniqueError


def login(email: str, password: str):
    user = UserModel.find_by_email(email=email)

    if user and check_encrypted_password(user.password, password):
        return user

    return None


def create_user(name: str, email: str, password: str):
    user = UserModel(
        name=name,
        email=email,
        password=encrypt_password(password),
    )

    try:
        user.validate()
        user.save()
        return user
    except NotUniqueError:
        raise UserAlreadyExists(message="User Already Exists")


def find_user(user_id: str):
    user = UserModel.find_by_id(user_id)
    if not user:
        raise UserNotFound(message="User Not Found")

    return user
