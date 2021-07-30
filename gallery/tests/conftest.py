import io
from os import environ
from uuid import uuid4

import pytest
from bson.objectid import ObjectId
from flask import Flask
from flask_jwt_extended import create_access_token
from werkzeug.datastructures import FileStorage
from gallery import exceptions, resources
from gallery.config import config_by_name
from gallery.documents import GalleryModel, PicturesModel, UserModel
from gallery.ext import auth, serializer
from mongoengine import connect, disconnect


@pytest.fixture()
def mock_env(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "other-secret-key")
    monkeypatch.setenv("FLASK_ENV", "testing")


@pytest.fixture()
def mongo():
    db = connect("mongoenginetest", host="mongomock://localhost")
    yield db
    db.drop_database("mongoenginetest")
    db.close()
    return


@pytest.fixture()
def app(mongo, mock_env):
    app = Flask(__name__)
    # load object-based default configuration
    env = environ.get("FLASK_ENV")
    app.config.from_object(config_by_name[env])

    auth.init_app(app)
    serializer.init_app(app)
    resources.init_app(app)

    exceptions.handle_api_exceptions(app)

    with app.app_context():
        yield app

    disconnect()


@pytest.fixture()
def create_user():
    id = ObjectId()
    user = UserModel(
        _id=id,
        name="name",
        email=f"{id}@email.com",
        password=auth.encrypt_password("ab@123dsf"),
    )
    return user.save()


@pytest.fixture()
def create_gallery(create_user):
    id = ObjectId()
    gallery = GalleryModel(_id=id, name="name", user=str(create_user._id))
    return gallery.save()


@pytest.fixture()
def gallery_with_pictures(create_user):
    pic_a = PicturesModel(id=uuid4(), name="01", url="url/1")
    pic_b = PicturesModel(id=uuid4(), name="02", url="url/2")
    id = ObjectId()

    gallery = GalleryModel(
        _id=id,
        name="name",
        user=str(create_user._id),
        pictures=[pic_a, pic_b],
    )
    return gallery.save()


@pytest.fixture()
def access_token(create_user):
    info = {"email": create_user.email, "id": str(create_user._id)}
    return create_access_token(info)


@pytest.fixture()
def token_with_invalid_user_id(create_user):
    info = {"email": create_user.email, "id": "abc123"}
    return create_access_token(info)


@pytest.fixture()
def token_with_invalid_user_id(create_user):
    info = {"email": "nao_tem_user@email.com", "id": "abc123"}
    return create_access_token(info)


@pytest.fixture()
def user():
    id = ObjectId()
    user = UserModel(
        _id=id,
        name="name",
        email=f"{id}@email.com",
        password=auth.encrypt_password("ab@123dsf"),
    )
    user = user.save()
    token = create_access_token({"email": user.email, "id": str(user._id)})

    pic_a = PicturesModel(id=uuid4(), name="01", url="url/1")
    pic_b = PicturesModel(id=uuid4(), name="02", url="url/2")

    gallery = GalleryModel(
        _id=ObjectId(),
        name="name",
        user=str(user._id),
        pictures=[pic_a, pic_b],
        can_approve=[str(user._id)],
    )
    gallery = gallery.save()

    return {
        "user": user,
        "access_token": token,
        "gallery": gallery,
    }


@pytest.fixture()
def file():
    return FileStorage(
        stream=io.BytesIO(b"my file contents"),
        filename="Input.jpg",
        content_type="jpg",
    )
