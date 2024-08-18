"""
* Initialization file for store api
"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

from dotenv import load_dotenv
from config import config

load_dotenv()

database = SQLAlchemy()
cache = Cache()

def create_app(config_name = os.getenv('FLASK_CONFIG') or 'default'):
    """
    * create app function for store api
    
    Keyword arguments:
    argument -- congfiguration
    Return: an app
    """

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)    

    database.init_app(app)
    cache.init_app(app)

    from .v1 import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix = "/v1")
    
    from app import models, schemas
    return app
