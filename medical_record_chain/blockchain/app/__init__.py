# app/__init__.py

import os

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config

db = SQLAlchemy()

def create_app(config_name):
    app = FlaskAPI(
                __name__,
                instance_path=os.path.join(os.path.abspath(os.curdir), 'instance'),
                instance_relative_config=True
                )
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    return app