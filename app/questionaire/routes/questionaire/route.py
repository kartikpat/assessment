from flask import  Flask,abort,jsonify
from . import questionaire
from ...service.questionaire import insert_questionaire, update_questionaire, get_questionaire_list, get_questionaire
from ...model.questionaire import Questionaire
from .validate import validate
from ....exception import BadContentType,InvalidObjectId, ValidationError, EmbeddedDocumentNotFound
import logging
from ....utils import get_data_in_dict, encode_objectId
logger = logging.getLogger(__name__)

@questionaire.route('/questionaire', methods=['GET'])
def fetch_all_questionaire():                
    try:
        data = get_questionaire_list()

        return jsonify({
                'status': 'success',
                'data': data
            })

    except Exception as e:
            logger.exception(e)
            message = ''
            abort(503,{'message': message})

@questionaire.route('/questionaire', methods=['POST'])
def create_questionaire():  
    try:
        data = get_data_in_dict()  

        validate(data, "insert")
         
        questionaire_id = insert_questionaire(data)

        questionaire_id = encode_objectId(questionaire_id)

        return jsonify({
            'status': 'success',
            'message': 'questionaire created successfully',
            'data': questionaire_id
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

    except (Questionaire.DoesNotExist, InvalidObjectId, EmbeddedDocumentNotFound) as e:
        logger.exception(e)
        message = 'questionaire id doesn\'t exist'
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
        data = get_questionaire(questionaire_id)

        return jsonify({
                'status': 'success',
                'data': data
            })

    except (Questionaire.DoesNotExist, InvalidObjectId) as e:
        logger.exception(e)
        message = 'questionaire id doesn\'t exist'
        if hasattr(e, 'message'):
            e.to_dict()
            message = e.message
        abort(404,{'message': message})       

    except Exception as e:
        logger.exception(e)
        message = ''
        abort(503,{'message': message})

            