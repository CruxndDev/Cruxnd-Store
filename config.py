from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config): pass

class ProductionConfig(Config): pass

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}