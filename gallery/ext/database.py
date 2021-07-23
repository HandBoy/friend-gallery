from flask_mongoengine import MongoEngine


def init_app(app):
    app.config["MONGODB_SETTINGS"] = {
        "db": app.config.DB,
        "host": app.config.DB_HOST,
    }
    MongoEngine(app)
