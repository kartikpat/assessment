from flask import  Flask, abort, jsonify
from . import jobAssociation
from ...service.jobAssociation import associateJobWithquestionaire, getAssociatedJobWithQuestionaire
from ...model.questionaire import Questionaire
from .validate import validate
from ....exception import BadContentType,InvalidObjectId, FormValidationError
import logging
from app.utils import get_data_in_dict
from mongoengine import * 
logger = logging.getLogger(__name__)

@jobAssociation.route('/questionaire/<questionaire_id>/job', methods=['GET'])
def fetch_job_associated_with_questionaire(questionaire_id):                
    try:
        data = getAssociatedJobWithQuestionaire(questionaire_id)

        return jsonify({
                'status': 'success',
                'data': data
            })

    except Exception as e:
            logger.exception(e)
            message = ''
            abort(503,{'message': message})

@jobAssociation.route('/questionaire/<questionaire_id>/job', methods=['POST'])
def associate_job_with_questionaire(questionaire_id):  
    try:
        data = get_data_in_dict()  

        validate(data)
         
        associateJobWithquestionaire(data, questionaire_id)

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

    except Questionaire.DoesNotExist as e:
        logger.exception(e)
        message = 'questionaire id doesn\'t exist'
        abort(404,{'message': message})
        
    except InvalidObjectId as e:
        logger.exception(e)
        message = 'questionaire id is not valid'
        if hasattr(e, 'message'):
            e.to_dict()
            message = e.message
        abort(404,{'message': message})           

    except Exception as e:
        logger.exception(e)
        message = ''
        abort(503,{'message': message})     