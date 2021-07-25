import pytest
from bson.objectid import ObjectId
from flask import Flask
from flask_jwt_extended import create_access_token
from gallery import resources
from gallery.documents import UserModel
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
        password=UserModel.encrypt_password("ab@123dsf"),
    )
    return user.save()


@pytest.fixture()
def access_token(create_user):
    user = create_user
    return create_access_token(identity=user.email)
