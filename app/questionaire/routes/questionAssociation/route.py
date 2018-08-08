from flask import  Flask, abort, jsonify
from . import questionAssociationWithQuestionaire
from ...service.questionAssociation import associate_question_with_questionaire
from ...model.questionaire import Questionaire
from .validate import validate
from ....exception import BadContentType,InvalidObjectId, FormValidationError
import logging
from app.utils import get_data_in_dict
from mongoengine import * 
logger = logging.getLogger(__name__)

@questionAssociationWithQuestionaire.route('/questionaire/<questionaire_id>/section/<section_id>/question', methods=['POST'])
def associateQuestionWithQuestionaire(questionaire_id, section_id):                
    try:
        data = get_data_in_dict()  

        validate(data)
         
        associate_question_with_questionaire(data, questionaire_id, section_id)

        return jsonify({
            'status': 'success',
            'message': 'questions associated successfully'
        })

    except (KeyError, BadContentType) as e:
        logger.exception(e)
        message = ''
        if hasattr(e, 'message'):
            e.to_dict()
            message = e.message
        abort(400,{'message': message}) 

    except (FormValidationError, ValidationError) as e: 
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

    