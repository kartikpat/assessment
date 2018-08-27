from flask import  Flask,request,abort,jsonify, current_app
from . import questions
from ...service.questions import insert_question, update_question, get_questions, get_question_by_id, checkAvailabiltyOfQuestion
from ...model.questions import Question
from .validate import validate
from ....exception import BadContentType,InvalidObjectId, FormValidationError, MissingGetParameters
import logging
from ....utils import get_data_in_dict, encode_objectId 
from mongoengine import *
logger = logging.getLogger(__name__)

@questions.route('/question', methods=['GET'])
def fetchQuestions():                 
    try:

        parameters = {}

        parameters["author"] = request.args.get("author")
        parameters["availability"] = request.args.get("availability")

        if not parameters["author"]:
            raise MissingGetParameters('author parameter is required')

        data = get_questions(parameters)

        return jsonify({
                'status': 'success',
                'data': data 
            }) 

    except MissingGetParameters as e:
        logger.exception(e)
        message = ''
        if hasattr(e, 'message'):
            e.to_dict()
            message = e.message
        abort(400,{'message': message})    

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

        question_id = encode_objectId(question_id)

        return jsonify({
            'status': 'success',
            'message': 'question created successfully',
            'data': question_id
        })

    # except NotUniqueError as e:    
    #     logger.exception(e)
    #     message = 'question text already exists'
    #     abort(409,{'message': message}) 

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

    except (FormValidationError, ValidationError) as e: 
        logger.exception(e)
        message = e.message
        abort(422,{'message': message}) 

    except Exception as e:
        logger.exception(e)
        print(e)
        message = ''
        abort(503,{'message': message}) 


@questions.route('/question/<question_id>', methods=['POST'])
def updateQuestion(question_id):
    try:
        
        data = get_data_in_dict()  

        validate(data, "update")

        if checkAvailabiltyOfQuestion(question_id):
            question_id = insert_question(data)
            question_id = encode_objectId(question_id)
            return jsonify({
                'status': 'success',
                'message': 'question inserted successfully',
                'data': question_id
            })    
        
        update_question(data, question_id)
        
        return jsonify({
            'status': 'success',
            'message': 'question updated successfully'
        })
        

    except (FormValidationError, ValidationError) as e: 
        logger.exception(e)
        message = e.message
        abort(422,{'message': message})     
    
    except KeyError as e:
        logger.exception(e)
        message = ''
        abort(400,{'message': message}) 

    except Question.DoesNotExist as e:
        logger.exception(e)
        message = 'question id doesn\'t exist'
        abort(404,{'message': message})
        
    except InvalidObjectId as e:
        logger.exception(e)
        message = 'question id is not valid'
        if hasattr(e, 'message'):
            e.to_dict()
            message = e.message
        abort(404,{'message': message})     

    except Exception as e:
        logger.exception(e)
        print(e)
        message = ''
        abort(503,{'message': message})            

@questions.route('/question/<question_id>', methods=['GET'])
def fetch_question(question_id):
    try:

        data = get_question_by_id(question_id)

        return jsonify({
                'status': 'success',
                'data': [data]
            })

    except Question.DoesNotExist as e:
        logger.exception(e)
        message = 'question id doesn\'t exist'
        abort(404,{'message': message})
        
    except InvalidObjectId as e:
        logger.exception(e)
        message = 'question id is not valid'
        if hasattr(e, 'message'):
            e.to_dict()
            message = e.message
        abort(404,{'message': message})        

    except Exception as e:
        logger.exception(e)
        message = ''
        abort(503,{'message': message})

            