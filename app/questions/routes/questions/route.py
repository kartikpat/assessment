from flask import  Flask,request,abort,jsonify, current_app
from . import questions
from ...service.questions import insert_question, update_question, get_questions_list, get_question
from ...model.questions import Question
from .validate import validate
from ....exception import BadContentType,InvalidObjectId, ValidationError, EmbeddedDocumentNotFound
import logging
from ....utils import get_data_in_dict
logger = logging.getLogger(__name__)


@questions.route('/question', methods=['GET'])
def fetch_all_questions():                
    try:
        data = get_questions_list()

        return jsonify({
                'status': 'success',
                'data': data
            })

    except Exception as e:
            logger.exception(e)
            message = ''
            abort(503,{'message': message})

@questions.route('/question', methods=['POST'])
def create_question():  
    try:
        data = get_data_in_dict()  

        validate(data, "insert")
         
        question_id = insert_question(data)

        return jsonify({
            'status': 'success',
            'message': 'question created successfully',
            'data': question_id
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

    except Exception as e:
        logger.exception(e)
        message = ''
        abort(503,{'message': message}) 


@questions.route('/question/<question_id>', methods=['POST'])
def updateQuestion(question_id):
    try:
        
        data = get_data_in_dict()  

        validate(data, "update")
        
        update_question(data, question_id)
        
        return jsonify({
            'status': 'success',
            'message': 'question updated successfully'
        })

    except ValidationError as e: 
        logger.exception(e)
        message = e.message
        abort(422,{'message': message})     
    
    except KeyError as e:
        logger.exception(e)
        message = ''
        abort(400,{'message': message}) 

    except (Question.DoesNotExist, InvalidObjectId, EmbeddedDocumentNotFound) as e:
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

@questions.route('/question/<question_id>', methods=['GET'])
def fetch_question(question_id):
    try:
        data = get_question(question_id)

        return jsonify({
                'status': 'success',
                'data': data
            })

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

            