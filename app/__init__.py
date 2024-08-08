"""
* Initialization file for store api
"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv
from config import config

load_dotenv()

database = SQLAlchemy()

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
    return
