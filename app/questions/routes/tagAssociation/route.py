from flask import  Flask,request,abort,jsonify, current_app
from . import tagAssociationWithQuestion
from app.questions.service.tagAssociation import update_tags_with_question, get_associated_tags_with_question
from app.questions.model.questions import Question
from app.questions.routes.tagAssociation.validate import validate
from app.exception import BadContentType,InvalidObjectId, ValidationError, EmbeddedDocumentNotFound
import logging
from app.utils import get_data_in_dict
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
            logger.debug(e)
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
        message = 'question id doesn\'t exist'
        if hasattr(e, 'message'):
            e.to_dict()
            message = e.message
        abort(404,{'message': message})    

    except Exception as e:
        logger.debug(e)
        message = ''
        abort(503,{'message': message})