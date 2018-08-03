from flask import  Flask,request,abort,jsonify, current_app
from . import questionResponse
from ...service.questionResponse import insert_questionResponse, update_questionResponse, get_questionResponse_list, get_questionResponse, questionResponse_exist
from ...model.questionResponse import QuestionResponse
from .validate import validate
from ....exception import BadContentType,InvalidObjectId, ValidationError, EmbeddedDocumentNotFound, MissingGetParameters
import logging
from ....utils import get_data_in_dict, encode_objectId
logger = logging.getLogger(__name__)

@questionResponse.route('/questionResponse', methods=['GET'])
def fetch_all_questionResponse():                
    try:
        parameters = {}

        parameters["associationPublished"] = request.args.get("associationPublished")
        parameters["invocation"] = request.args.get("invocation")
        parameters["seeker"] = request.args.get("seeker")

        if not parameters["associationPublished"]:
            raise MissingGetParameters('associationPublished parameter is required')

        if not parameters["invocation"]:
            raise MissingGetParameters('invocation parameter is required')

        if not parameters["seeker"]:
            raise MissingGetParameters('seeker parameter is required')    

        data = get_questionResponse_list(parameters)

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

@questionResponse.route('/questionResponse', methods=['POST'])
def create_questionResponse():  
    try:
        data = get_data_in_dict() 
        validate(data, "insert")
        questionResponse_id = None

        if "associationPublished" in data and "invocation" in data and "seeker" in data:
            questionResponse_id = questionResponse_exist(data)
        
        if not questionResponse_id: 
            questionResponse_id = insert_questionResponse(data)
        else:
            update_questionResponse(data, encode_objectId(questionResponse_id))  
            return jsonify({
                'status': 'success',
                'message': 'questionResponse updated successfully',
                'data': encode_objectId(questionResponse_id)
            })

        questionResponse_id = encode_objectId(questionResponse_id)

        return jsonify({
            'status': 'success',
            'message': 'questionResponse created successfully',
            'data': questionResponse_id
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
#         logger.exception(e)
#         message = e.message
#         abort(422,{'message': message})     
    
#     except KeyError as e:
#         logger.exception(e)
#         message = ''
#         abort(400,{'message': message}) 

#     except (Questionaire.DoesNotExist, InvalidObjectId, EmbeddedDocumentNotFound) as e:
#         logger.exception(e)
#         message = 'questionResponse id doesn\'t exist'
#         if hasattr(e, 'message'):
#             e.to_dict()
#             message = e.message
#         abort(404,{'message': message})    

#     except Exception as e:
#         logger.exception(e)
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
        logger.exception(e)
        message = 'questionResponse id doesn\'t exist'
        if hasattr(e, 'message'):
            e.to_dict()
            message = e.message
        abort(404,{'message': message})       

    except Exception as e:
        logger.exception(e)
        message = ''
        abort(503,{'message': message})

            