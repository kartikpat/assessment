from flask import  Flask,abort,jsonify, request
from . import questionaire
from ...service.questionaire import insert_questionaire, update_questionaire, get_questionaire, get_questionaire_by_id, questionaire_exist
from ...model.questionaire import Questionaire
from .validate import validate
from ....exception import BadContentType,InvalidObjectId, ValidationError, MissingGetParameters
import logging
from ....utils import get_data_in_dict, encode_objectId
logger = logging.getLogger(__name__)

@questionaire.route('/questionaire', methods=['GET'])
def fetchQuestionaire():                 
    try:
 
        parameters = {}

        parameters["associationMeta"] = request.args.get("associationMeta")
        parameters["associationPublished"] = request.args.get("associationPublished")
        parameters["invocation"] = request.args.get("invocation")
        parameters["seeker"] = request.args.get("seeker")

        parameters["association"] = parameters["associationMeta"] or parameters["associationPublished"]
        
        if not parameters["association"]:
            raise MissingGetParameters('association parameter is required')    

        data = get_questionaire(parameters)

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

@questionaire.route('/questionaire', methods=['POST'])
def create_questionaire():  
    try:
        data = get_data_in_dict()  

        questionaire_id = None

        if "associationMeta" in data and "invocation" in data:
            questionaire_id = questionaire_exist(data)

        if questionaire_id:
            questionaire_id = encode_objectId(questionaire_id)
            return jsonify({
                'status': 'success',
                'message': 'questionaire already associated with job',
                'data': questionaire_id
            })
        
        validate(data, "insert") 
        questionaire_id = insert_questionaire(data)

        questionaire_id = encode_objectId(questionaire_id)

        return jsonify({
            'status': 'success',
            'message': 'questionaire created successfully',
            'data': questionaire_id
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

    except ValidationError as e: 
        logger.exception(e)
        message = e.message
        abort(422,{'message': message}) 

    except Exception as e:
        logger.exception(e)
        message = ''
        abort(503,{'message': message})        


@questionaire.route('/questionaire/<questionaire_id>', methods=['POST'])
def updateQuestionaire(questionaire_id):
    try:
        
        data = get_data_in_dict()
        
        validate(data, "update")
        
        update_questionaire(data, questionaire_id)
        
        return jsonify({
            'status': 'success',
            'message': 'questionaire updated successfully'
        })

    except ValidationError as e: 
        logger.exception(e)
        message = e.message
        abort(422,{'message': message})     
    
    except KeyError as e:
        logger.exception(e)
        message = ''
        abort(400,{'message': message}) 

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

@questionaire.route('/questionaire/<questionaire_id>', methods=['GET'])
def fetch_questionaire(questionaire_id):
    try:
        data = get_questionaire_by_id(questionaire_id)

        return jsonify({
                'status': 'success',
                'data': data
            })

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

            