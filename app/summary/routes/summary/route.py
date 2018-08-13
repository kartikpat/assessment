from flask import  Flask,request,abort,jsonify, current_app
from . import summary
from ...service.summary import insert_summary, update_summary, get_summary_list, get_summary
from ...model.summary import Summary
from .validate import validate
from ....exception import BadContentType,InvalidObjectId, FormValidationError, EmbeddedDocumentNotFound
import logging
from ....utils import get_data_in_dict
logger = logging.getLogger(__name__)


@summary.route('/summary', methods=['GET'])
def fetch_all_summary():                
    try:
        data = get_summary_list()

        return jsonify({
                'status': 'success',
                'data': data
            })

    except Exception as e:
            logger.exception(e)
            message = ''
            abort(503,{'message': message})

@summary.route('/summary', methods=['POST'])
def create_summary():  
    try:
        data = get_data_in_dict()  

        validate(data, "insert")
         
        summary_id = insert_summary(data)

        return jsonify({
            'status': 'success',
            'message': 'summary created successfully',
            'data': summary_id
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

    except Exception as e:
        logger.exception(e)
        message = ''
        abort(503,{'message': message}) 


# @summary.route('/summary/<summary_id>', methods=['POST'])
# def updateQuestion(summary_id):
#     try:
        
#         data = get_data_in_dict()  

#         validate(data, "update")
        
#         update_summary(data, summary_id)
        
#         return jsonify({
#             'status': 'success',
#             'message': 'summary updated successfully'
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
#         message = 'summary id doesn\'t exist'
#         if hasattr(e, 'message'):
#             e.to_dict()
#             message = e.message
#         abort(404,{'message': message})    

#     except Exception as e:
#         logger.exception(e)
#         message = ''
#         abort(503,{'message': message})            

@summary.route('/summary/<summary_id>', methods=['GET'])
def fetch_summary(summary_id):
    try:
        data = get_summary(summary_id)

        return jsonify({
                'status': 'success',
                'data': data
            })

    except (Summary.DoesNotExist, InvalidObjectId) as e:
        logger.exception(e)
        message = 'summary id doesn\'t exist'
        if hasattr(e, 'message'):
            e.to_dict()
            message = e.message
        abort(404,{'message': message})       

    except Exception as e:
        logger.exception(e)
        message = ''
        abort(503,{'message': message})

            