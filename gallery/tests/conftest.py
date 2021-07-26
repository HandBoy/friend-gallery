from uuid import uuid4

import pytest
from bson.objectid import ObjectId
from flask import Flask
from flask_jwt_extended import create_access_token
from gallery import exceptions, resources
from gallery.documents import GalleryModel, PicturesModel, UserModel
from gallery.ext import auth, configuration, serializer
from mongoengine import connect, disconnect


@pytest.fixture(scope="session")
def mongo():
    db = connect("mongoenginetest", host="mongomock://localhost")
    yield db
    db.drop_database("mongoenginetest")
    db.close()
    return


@pytest.fixture(scope="session")
def app(mongo):
    app = Flask(__name__)
    configuration.init_app(app, FORCE_ENV_FOR_DYNACONF="testing")
    auth.init_app(app)
    serializer.init_app(app)
    resources.init_app(app)

    exceptions.handle_api_exceptions(app)

    with app.app_context():
        yield app

    disconnect()


@pytest.fixture(scope="function")
def create_user():
    id = ObjectId()
    user = UserModel(
        _id=id,
        name="name",
        email=f"{id}@email.com",
        password=auth.encrypt_password("ab@123dsf"),
    )
    return user.save()


@pytest.fixture(scope="function")
def create_gallery(create_user):
    id = ObjectId()
    gallery = GalleryModel(_id=id, name="name", user=str(create_user._id))
    return gallery.save()


@pytest.fixture(scope="function")
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
