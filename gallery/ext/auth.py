from flask_jwt_extended import JWTManager
from datetime import timedelta


def init_app(app):
    app.config["JWT_SECRET_KEY"] = app.config.SECRET_KEY
    app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=1800)
    JWTManager(app)
