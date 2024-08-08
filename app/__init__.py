from config import config
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app(config_name = os.getenv('FLASK_CONFIG') or 'default'):	
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    return app