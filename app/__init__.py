# third-party imports
from flask import Flask
from flask_mongoengine import MongoEngine
import logging, json
import logging.handlers, logging.config

# local imports
from config import app_config
from .error import *

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
 
    if(configInstance.FLASK_LOGGING):
        with open("loggingConfiguration.json", 'r') as logging_configuration_file:
            config_dict = json.load(logging_configuration_file)

        logging.config.dictConfig(config_dict)
       
    #questionaire blueprints registration
    from .questionaire.routes.jobAssociation import jobAssociation as jobAssociation_route
    app.register_blueprint(jobAssociation_route, url_prefix=configInstance.FLASK_API_VERSION)

    from .questionaire.routes.questionaire import questionaire as questionaire_route
    app.register_blueprint(questionaire_route, url_prefix=configInstance.FLASK_API_VERSION)

    from .questionaire.routes.tagAssociation import tagAssociationWithQuestionaire as tagAssociationWithQuestionaire_route
    app.register_blueprint(tagAssociationWithQuestionaire_route, url_prefix=configInstance.FLASK_API_VERSION)

    #questions blueprints registration
    from .questions.routes.questions import questions as questions_route
    app.register_blueprint(questions_route, url_prefix=configInstance.FLASK_API_VERSION)

    from .questions.routes.tagAssociation import tagAssociationWithQuestion as tagAssociationWithQuestion_route
    app.register_blueprint(tagAssociationWithQuestion_route, url_prefix=configInstance.FLASK_API_VERSION)

    #summary blueprints registration
    from .summary.routes.summary import summary as summary_route
    app.register_blueprint(summary_route, url_prefix=configInstance.FLASK_API_VERSION)

    #questionResponse blueprints registration
    from .questionResponse.routes.questionResponse import questionResponse as questionResponse_route
    app.register_blueprint(questionResponse_route, url_prefix=configInstance.FLASK_API_VERSION)

    from .task.worker import celery_worker as celery_worker_blueprint
    app.register_blueprint(celery_worker_blueprint, url_prefix='/task')

    # error handlers registration 
    app.register_error_handler(404, not_found)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(503, service_error)
    app.register_error_handler(422, unprocessable_entity)

    return app
