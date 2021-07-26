from datetime import timedelta
from gallery.documents import UserModel

from flask_jwt_extended import JWTManager
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000,
)


def encrypt_password(password):
    return pwd_context.encrypt(password)


def check_encrypted_password(pass_hash, password):
    return pwd_context.verify(password, pass_hash)


def init_app(app):
    app.config["JWT_SECRET_KEY"] = app.config.SECRET_KEY
    app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=1800)
    jwt = JWTManager(app)

    # Register a callback function that loades a user from your database
    # whenever a protected route is accessed.
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]["id"]
        return UserModel.find_by_id(user_id=identity)
