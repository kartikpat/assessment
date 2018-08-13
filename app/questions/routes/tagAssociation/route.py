from flask import  Flask,request,abort,jsonify, current_app
from . import tagAssociationWithQuestion
from ...service.tagAssociation import update_tags_with_question, get_associated_tags_with_question
from ...model.questions import Question
from .validate import validate
from ....exception import BadContentType, InvalidObjectId, FormValidationError, EmbeddedDocumentNotFound
import logging
from ....utils import get_data_in_dict
logger = logging.getLogger(__name__)

@tagAssociationWithQuestion.route('/question/<question_id>/tag', methods=['GET'])
def fetch_tags_associated_with_question(question_id):                
    try:
        data = get_associated_tags_with_question(question_id)

        return jsonify({
                'status': 'success',
                'data': data
            })

    except Exception as e:
            logger.exception(e)
            message = ''
            abort(503,{'message': message})

@tagAssociationWithQuestion.route('/question/<question_id>/tag', methods=['POST'])
def associate_tags_with_question(question_id):  
    try:
        data = get_data_in_dict()  

        validate(data)
         
        update_tags_with_question(data, question_id)

        return jsonify({
            'status': 'success',
            'message': 'tags associated successfully'
        })

    except (KeyError, BadContentType) as e:
        logger.exception(e)
        message = ''
        if hasattr(e, 'message'):
            e.to_dict()
            message = e.message
        abort(400,{'message': message}) 

    except FormValidationError as e: 
        logger.exception(e)
        message = e.message
        abort(422,{'message': message})  

    except (Question.DoesNotExist, InvalidObjectId) as e:
        logger.exception(e)
        message = 'question id doesn\'t exist'
        if hasattr(e, 'message'):
            e.to_dict()
            message = e.message
        abort(404,{'message': message})    

    except Exception as e:
        logger.exception(e)
        message = ''
        abort(503,{'message': message})