from flask import  Flask,abort,jsonify, request
from . import questionnaire
from ...service.questionnaire import insert_questionnaire, update_questionnaire, get_questionnaire, get_questionnaire_by_id, questionnaire_exist
from ...model.questionnaire import Questionnaire
from .validate import validate 
from ....exception import BadContentType,InvalidObjectId, FormValidationError, MissingGetParameters, NotAuthorized
import logging
from ....utils import get_data_in_dict, encode_objectId, isAuthorized
from mongoengine import *
logger = logging.getLogger(__name__)

@questionnaire.route('/questionnaire', methods=['GET'])
def fetchQuestionnaire():                 
    try:

        # is_auth, payload = isAuthorized()

        # if not is_auth:
        #     raise NotAuthorized('') 
        
        parameters = {}

        parameters["associationMeta"] = request.args.get("associationMeta")
        parameters["associationPublished"] = request.args.get("associationPublished")
        parameters["invocation"] = request.args.get("invocation")
        parameters["seeker"] = request.args.get("seeker")

        parameters["association"] = parameters["associationMeta"] or parameters["associationPublished"]
        
        if not parameters["association"]:
            raise MissingGetParameters('association parameter is required')    

        data = get_questionnaire(parameters)

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

    except NotAuthorized as e:
        logger.exception(e)
        message = ''
        if hasattr(e, 'message'):
            e.to_dict()
            message = e.message
        abort(403,{'message': message})              

    except Exception as e:
            logger.exception(e)
            message = ''
            abort(503,{'message': message})

@questionnaire.route('/questionnaire', methods=['POST'])
def create_questionnaire():  
    try:
        data = get_data_in_dict()  

        questionnaire_id = None

        if "associationMeta" in data and "invocation" in data:
            questionnaire_id = questionnaire_exist(data)

        if questionnaire_id:
            questionnaire_id = encode_objectId(questionnaire_id)
            return jsonify({
                'status': 'success',
                'message': 'questionnaire already associated with job',
                'data': questionnaire_id
            })
        
        validate(data, "insert") 
        questionnaire_id = insert_questionnaire(data)

        questionnaire_id = encode_objectId(questionnaire_id)

        return jsonify({
            'status': 'success',
            'message': 'questionnaire created successfully',
            'data': questionnaire_id
        })   

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
        message = ''
        abort(503,{'message': message})        


@questionnaire.route('/questionnaire/<questionnaire_id>', methods=['POST'])
def updateQuestionnaire(questionnaire_id):
    try:
        
        data = get_data_in_dict()
        
        validate(data, "update")
        
        update_questionnaire(data, questionnaire_id)
        
        return jsonify({
            'status': 'success',
            'message': 'questionnaire updated successfully'
        })

    except (FormValidationError, ValidationError) as e: 
        logger.exception(e)
        message = e.message
        abort(422,{'message': message})     
    
    except KeyError as e:
        logger.exception(e)
        message = ''
        abort(400,{'message': message}) 

    except Questionnaire.DoesNotExist as e:
        logger.exception(e)
        message = 'questionnaire id doesn\'t exist'
        abort(404,{'message': message})
        
    except InvalidObjectId as e:
        logger.exception(e)
        message = 'questionnaire id is not valid'
        if hasattr(e, 'message'):
            e.to_dict()
            message = e.message
        abort(404,{'message': message})           

    except Exception as e:
        logger.exception(e)
        message = ''
        abort(503,{'message': message})            

@questionnaire.route('/questionnaire/<questionnaire_id>', methods=['GET'])
def fetch_questionnaire(questionnaire_id):
    try:
        data = get_questionnaire_by_id(questionnaire_id)

        return jsonify({
                'status': 'success',
                'data': data
            })

    except Questionnaire.DoesNotExist as e:
        logger.exception(e)
        message = 'questionnaire id doesn\'t exist'
        abort(404,{'message': message})
        
    except InvalidObjectId as e:
        logger.exception(e)
        message = 'questionnaire id is not valid'
        if hasattr(e, 'message'):
            e.to_dict()
            message = e.message
        abort(404,{'message': message})        

    except Exception as e:
        logger.exception(e)
        message = ''
        abort(503,{'message': message})

            