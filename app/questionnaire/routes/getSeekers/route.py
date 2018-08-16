from flask import  Flask, abort, jsonify
from . import getSeekers
from ....questionResponse.service.getSeekers import get_seekers
from ....exception import BadContentType,InvalidObjectId, FormValidationError, NotAuthorized
from ...model.questionnaire import Questionnaire
import logging
from ....utils import get_data_in_dict, encode_objectId
from .validate import validate
from mongoengine import * 
logger = logging.getLogger(__name__)

@getSeekers.route('/questionnaire/seekers', methods=['POST'])
def fetch_seekers_with_given_reponses():                
    try:

        # is_auth, payload = isAuthorized()

        # if not is_auth:
        #     raise NotAuthorized('') 

        data = get_data_in_dict()  

        validate(data)
        
        for index, section in enumerate(data["questionnaire"]):
            seekers = get_seekers(data["associationPublished"], section["questions"], section["invocation"])

        return jsonify({
                'status': 'success',
                'data': seekers
            })

    except (FormValidationError, ValidationError) as e: 
        logger.exception(e)
        message = e.message
        abort(422,{'message': message})     
    
    except KeyError as e:
        logger.exception(e)
        message = ''
        abort(400,{'message': message}) 

    except Questionnaire.DoesNotExist as e:
        logger.exception(e)
        message = 'questionnaire id doesn\'t exist'
        abort(404,{'message': message})

    except NotAuthorized as e:
        logger.exception(e)
        message = ''
        if hasattr(e, 'message'):
            e.to_dict()
            message = e.message
        abort(403,{'message': message})    
        
    except InvalidObjectId as e:
        logger.exception(e)
        message = 'questionnaire id is not valid'
        if hasattr(e, 'message'):
            e.to_dict()
            message = e.message
        abort(404,{'message': message})           

    except Exception as e:
        logger.exception(e)
        message = ''
        abort(503,{'message': message})