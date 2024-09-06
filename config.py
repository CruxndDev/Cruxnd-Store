from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URI")
    CACHE_TYPE = os.getenv("DEV_CACHE_TYPE")
    CACHE_REDIS_HOST = os.getenv("CACHE_REDIS_HOST")
    CACHE_REDIS_PORT = os.getenv("CACHE_REDIS_PORT")
    CACHE_DEFAULT_TIMEOUT = os.getenv("CACHE_REDIS_TIMEOUT")


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("TESTING_DATABASE_URI")
    CACHE_TYPE = os.getenv("TESTING_CACHE_TYPE")
    CACHE_DEFAULT_TIMEOUT = os.getenv("TESTING_CACHE_DEFAULT_TIMEOUT")


class ProductionConfig(Config):
    pass


config = {
    "testing": TestingConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
