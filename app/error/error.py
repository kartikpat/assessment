
from flask import make_response,jsonify
import logging
logger = logging.getLogger(__name__)

def not_found(error):
    logger.debug(error)
    message = error.description['message']
    if(message == ''): 
        message = 'not found'

    return make_response(jsonify({
    'error': message,
    'status': 'fail'
    }), 404) 

def forbidden(error):
    logger.debug(error)
    message = error.description['message']
    if(message == ''): 
        message = 'forbidden'

    return make_response(jsonify({
    'error': message,
    'status': 'fail'
    }), 403)

def bad_request(error):
    logger.debug(error)
    message = error.description['message']
    if(message == ''): 
        message = 'bad request'

    return make_response(jsonify({
    'error': message,
    'status': 'fail'
    }), 400)  

def unprocessable_entity(error):
    logger.debug(error)
    message = error.description['message']
    if(message == ''): 
        message = 'missing parameters'

    return make_response(jsonify({
    'error': message,
    'status': 'fail'
    }), 422) 

def service_error(error):
    logger.debug(error)
    message = error.description['message']
    if(message == ''): 
        message = 'service unavailable'

    return make_response(jsonify({
    'error': message,
    'status': 'fail'
    }), 503)         