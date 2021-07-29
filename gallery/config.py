from os import environ


class BaseConfig:
    DEBUG = False
    TESTING = False
    DB = environ.get("DB")
    DB_HOST = environ.get("DB_HOST")
    SECRET_KEY = environ.get("SECRET_KEY")

    AWS_ACCESS_KEY_ID = environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_DEFAULT_REGION = environ.get("AWS_DEFAULT_REGION")
    AWS_S3_LOCATION = environ.get("AWS_S3_LOCATION")
    AWS_S3_BUCKET_NAME = environ.get("AWS_S3_BUCKET_NAME")

    TOKEN_EXPIRES = environ.get("TOKEN_EXPIRES", 120)


class ProductionConfig(BaseConfig):
    ENV = "production"
    LOG_LEVEL = "INFO"


class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class TestingConfig(BaseConfig):
    ENV = "test"
    TESTING = True
    LOG_LEVEL = "DEBUG"
    SECRET_KEY = environ.get("SECRET_KEY", "other-secret-key")


config_by_name = dict(
    production=ProductionConfig,
    development=DevelopmentConfig,
    testing=TestingConfig,
)
