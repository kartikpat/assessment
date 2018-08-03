import os

# third-party imports
from flask import Flask

# local imports
from config import app_config
from app.task.celery import make_celery

config_name = os.getenv('FLASK_CONFIG') or 'development'

flask_app = Flask(__name__, instance_relative_config=True)
flask_app.config.from_object(app_config[config_name])
configInstance = app_config[config_name]()
flask_app.config.from_pyfile(configInstance.FLASK_CONFIG)

celery = make_celery(flask_app)

@celery.task()
def add_together(a, b):
    return a + b