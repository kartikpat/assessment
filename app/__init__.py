# third-party imports
from flask import Flask
from flask_mongoengine import MongoEngine
import logging, json
import logging.handlers, logging.config

# local imports
from config import app_config
from .error.error import *
from .task.celery import make_celery

# db variable initialization
db = MongoEngine()

def create_app(config_name):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'development')
       
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    configInstance = app_config[config_name]()
    app.config.from_pyfile(configInstance.FLASK_CONFIG)
    db.init_app(app)
 
    celery = make_celery(app)
    if(configInstance.FLASK_LOGGING):
        with open("loggingConfiguration.json", 'r') as logging_configuration_file:
            config_dict = json.load(logging_configuration_file)

        logging.config.dictConfig(config_dict)
       
        
    # blueprints registration
    from .controller.assessment.operation import operation as assessment_operation_blueprint
    app.register_blueprint(assessment_operation_blueprint, url_prefix=configInstance.FLASK_API_VERSION)

    # from .task import task as task_blueprint
    # app.register_blueprint(task_blueprint, url_prefix='/tasks')

    # error handlers registration 
    app.register_error_handler(404, not_found)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(503, service_error)
    app.register_error_handler(422, unprocessable_entity)
    return app
