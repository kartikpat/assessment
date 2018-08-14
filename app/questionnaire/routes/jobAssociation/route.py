from flask import  Flask, abort, jsonify
from . import jobAssociation
from ...service.jobAssociation import associateJobWithquestionnaire, getAssociatedJobWithQuestionnaire
from ...model.questionnaire import Questionnaire
from .validate import validate
from ....exception import BadContentType,InvalidObjectId, FormValidationError
import logging
from app.utils import get_data_in_dict
from mongoengine import * 
logger = logging.getLogger(__name__)

@jobAssociation.route('/questionnaire/<questionnaire_id>/job', methods=['GET'])
def fetch_job_associated_with_questionnaire(questionnaire_id):                
    try:
        data = getAssociatedJobWithQuestionnaire(questionnaire_id)

        return jsonify({
                'status': 'success',
                'data': data
            })

    except Exception as e:
            logger.exception(e)
            message = ''
            abort(503,{'message': message})

@jobAssociation.route('/questionnaire/<questionnaire_id>/job', methods=['POST'])
def associate_job_with_questionnaire(questionnaire_id):  
    try:
        data = get_data_in_dict()  

        validate(data)
         
        associateJobWithquestionnaire(data, questionnaire_id)

        return jsonify({
            'status': 'success',
            'message': 'job associated successfully'
        })

    except (FormValidationError, ValidationError) as e: 
        logger.exception(e)
        message = e.message
        abort(422,{'message': message})     
    
    except KeyError as e:
        logger.exception(e.args[0])
        message = e.args[0] + ' key missing';
        abort(400,{'message': message})    

    except BadContentType as e:
        logger.exception(e)
        message = ''
        if hasattr(e, 'message'):
            e.to_dict()
            message = e.message
        abort(400,{'message': message}) 

    except Questionnaire.DoesNotExist as e:
        logger.exception(e)
        message = 'questionnaire id doesn\'t exist'
        abort(404,{'message': message})
        
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