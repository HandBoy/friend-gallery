from mongoengine.errors import NotUniqueError

from gallery.documents import GaleryModel, UserModel
from gallery.exceptions import UserAlreadyExists, UserNotFound


def login(email: str, password: str):
    user = UserModel.find_by_email(email=email)

    if user and user.check_encrypted_password(password):
        return True

    return False


def create_user(name: str, email: str, password: str):
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


def find_user(user_id: str):
    user = UserModel.find_by_id(user_id)
    if not user:
        raise UserNotFound(message="User Not Found")

    return user


def create_galery(user: UserModel, raw_galery: dict):
    galery = GaleryModel(**raw_galery)
    user.save()
    galery.user = user.to_dbref()

    galery.save()
