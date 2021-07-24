from datetime import timedelta

from flask_jwt_extended import JWTManager
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000,
)


def init_app(app):
    app.config["JWT_SECRET_KEY"] = app.config.SECRET_KEY
    app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=1800)
    JWTManager(app)
