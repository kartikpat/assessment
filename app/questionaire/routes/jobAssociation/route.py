from flask import  Flask, abort, jsonify
from . import jobAssociation
from ...service.jobAssociation import associateJobWithQuestionaire, get_associated_job_list_with_questionaire
from ...model.questionaire import Questionaire
from .validate import validate
from ....exception import BadContentType,InvalidObjectId, ValidationError
import logging
from app.utils import get_data_in_dict
logger = logging.getLogger(__name__)

@jobAssociation.route('/questionaire/<questionaire_id>/job', methods=['GET'])
def fetch_job_associated_with_questionaire(questionaire_id):                
    try:
        data = get_associated_job_list_with_questionaire(questionaire_id)

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
         
        associateJobWithQuestionaire(data, questionaire_id)

        return jsonify({
            'status': 'success',
            'message': 'job associated successfully'
        })

    except (KeyError, BadContentType) as e:
        logger.exception(e)
        message = ''
        if hasattr(e, 'message'):
            e.to_dict()
            message = e.message
        abort(400,{'message': message}) 

    except ValidationError as e: 
        logger.exception(e)
        message = e.message
        abort(422,{'message': message})  

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