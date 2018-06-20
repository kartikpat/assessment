from flask import  Flask,request,abort,jsonify, current_app
from . import jobAssociation
from app.questionaire.service.jobAssociation import associate_job_list_with_questionaire, get_associated_job_list_with_questionaire
from app.questionaire.model.questionaire import Questionaire
from app.questionaire.routes.jobAssociation.validate import validate
from app.exception import BadContentType,InvalidObjectId, ValidationError
import logging
from app.utils import get_data_in_dict
logger = logging.getLogger(__name__)

@jobAssociation.route('/questionaire/<questionaire_id>/job', methods=['GET'])
def fetch_job_associated_with_questionaire(questionaireaire_id):                
    try:
        data = get_associated_job_list_with_questionaire(questionaire_id)

        return jsonify({
                'status': 'success',
                'data': data
            })

    except Exception as e:
            logger.debug(e)
            message = ''
            abort(503,{'message': message})

@jobAssociation.route('/questionaire/<questionaire_id>/tag', methods=['POST'])
def associate_job_with_questionaire(questionaire_id):  
    try:
        data = get_data_in_dict()  

        validate(data)
         
        associate_job_list_with_questionaire(data, questionaire_id)

        return jsonify({
            'status': 'success',
            'message': 'jobs associated successfully'
        })

    except (KeyError, BadContentType) as e:
        logger.debug(e)
        message = ''
        if hasattr(e, 'message'):
            e.to_dict()
            message = e.message
        abort(400,{'message': message}) 

    except ValidationError as e: 
        logger.debug(e)
        message = e.message
        abort(422,{'message': message})  

    except (Question.DoesNotExist, InvalidObjectId) as e:
        logger.debug(e)
        message = 'questionaire id doesn\'t exist'
        if hasattr(e, 'message'):
            e.to_dict()
            message = e.message
        abort(404,{'message': message})    

    except Exception as e:
        logger.debug(e)
        message = ''
        abort(503,{'message': message})