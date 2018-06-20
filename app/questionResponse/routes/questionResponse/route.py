from flask import  Flask,request,abort,jsonify, current_app
from . import questionResponse
from app.questionResponse.service.questionResponse import insert_questionResponse, update_questionResponse, get_questionResponse_list, get_questionResponse
from app.questionResponse.model.questionResponse import QuestionResponse
from app.questionResponse.routes.questionResponse.validate import validate
from app.exception import BadContentType,InvalidObjectId, ValidationError, EmbeddedDocumentNotFound
import logging
from app.utils import get_data_in_dict
logger = logging.getLogger(__name__)


@questionResponse.route('/questionResponse', methods=['GET'])
def fetch_all_questionResponse():                
    try:
        data = get_questionResponse_list()

        return jsonify({
                'status': 'success',
                'data': data
            })

    except Exception as e:
            logger.debug(e)
            message = ''
            abort(503,{'message': message})

@questionResponse.route('/questionResponse', methods=['POST'])
def create_questionResponse():  
    try:
        data = get_data_in_dict()  

        validate(data, "insert")
         
        questionResponse_id = insert_questionResponse(data)

        return jsonify({
            'status': 'success',
            'message': 'questionResponse created successfully',
            'data': questionResponse_id
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

    except Exception as e:
        logger.debug(e)
        message = ''
        abort(503,{'message': message}) 


# @questionResponse.route('/questionResponse/<questionResponse_id>', methods=['POST'])
# def updateQuestion(questionResponse_id):
#     try:
        
#         data = get_data_in_dict()  

#         validate(data, "update")
        
#         update_questionResponse(data, questionResponse_id)
        
#         return jsonify({
#             'status': 'success',
#             'message': 'questionResponse updated successfully'
#         })

#     except ValidationError as e: 
#         logger.debug(e)
#         message = e.message
#         abort(422,{'message': message})     
    
#     except KeyError as e:
#         logger.debug(e)
#         message = ''
#         abort(400,{'message': message}) 

#     except (Questionaire.DoesNotExist, InvalidObjectId, EmbeddedDocumentNotFound) as e:
#         logger.debug(e)
#         message = 'questionResponse id doesn\'t exist'
#         if hasattr(e, 'message'):
#             e.to_dict()
#             message = e.message
#         abort(404,{'message': message})    

#     except Exception as e:
#         logger.debug(e)
#         message = ''
#         abort(503,{'message': message})            

@questionResponse.route('/questionResponse/<questionResponse_id>', methods=['GET'])
def fetch_questionResponse(questionResponse_id):
    try:
        data = get_questionResponse(questionResponse_id)

        return jsonify({
                'status': 'success',
                'data': data
            })

    except (QuestionResponse.DoesNotExist, InvalidObjectId) as e:
        logger.debug(e)
        message = 'questionResponse id doesn\'t exist'
        if hasattr(e, 'message'):
            e.to_dict()
            message = e.message
        abort(404,{'message': message})       

    except Exception as e:
        logger.debug(e)
        message = ''
        abort(503,{'message': message})

            