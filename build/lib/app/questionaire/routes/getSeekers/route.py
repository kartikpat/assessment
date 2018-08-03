from flask import  Flask, abort, jsonify
from . import getSeekers
from ....questionResponse.service.getSeekers import get_seekers
from ....exception import BadContentType,InvalidObjectId, ValidationError
from ...model.questionaire import Questionaire
import logging
from ....utils import get_data_in_dict, encode_objectId
from .validate import validate
logger = logging.getLogger(__name__)

@getSeekers.route('/questionaire/<questionaire_id>/seekers', methods=['POST'])
def fetch_seekers_with_given_reponses(questionaire_id):                
    try:

        data = get_data_in_dict()  

        validate(data)

        seekers = get_seekers(questionaire_id, data["questions"])

        return jsonify({
                'status': 'success',
                'data': seekers
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