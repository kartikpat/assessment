from flask import  Flask,request,abort,jsonify, current_app
from . import operation
from app.service.assessment.service import create_assessment, update_assessment, fetch_assessment_list, fetch_assessment
from app.model.assessment.model import Assessment
from app.validate.assessment.validate import AssessmentForm
from app.error.exception import ValidationError, InvalidObjectId
import logging
logger = logging.getLogger(__name__)

@operation.route('/assessment', methods=['GET', 'POST'])
def fetch_list_assessment_or_create_assessment():
    if request.method == 'POST':  
        try:
            assessment_form = AssessmentForm(request.form)
            if(not assessment_form.validate()):
                for fieldName, errorMessage in assessment_form.errors.items():
                    raise ValidationError(''+fieldName+' : '+errorMessage[0]+'')
            data = {
                "name": request.form['name'],
                "status": request.form['status'],
                "type": request.form['type'],
                "assessor": request.form['assessor'],
                "created": request.form['created'],
                "lastUpdated": request.form['lastUpdated'],
                "durationInMin": request.form['durationInMin'],
                "security": request.form['security'],
                "invocation": request.form['invocation'],
                "expiry": request.form['expiry'],
                "quesbankType": request.form['quesbankType'],
                "description": request.form['description'],
                "instruction": request.form['instruction']
            }    
            
            assessment_id = create_assessment(data)

            return jsonify({
                'status': 'success',
                'message': 'assessment created successfully',
                'data': assessment_id
            })
        
        except KeyError as e:
            message = ''
            abort(400,{'message': message}) 

        except ValidationError as e: 
            message = e.message
            abort(422,{'message': message}) 

        except Exception as e:
            message = ''
            abort(503,{'message': message}) 
                
    try:
        data = fetch_assessment_list()

        return jsonify({
                'status': 'success',
                'data': data
            })

    except Exception as e:
            message = ''
            abort(503,{'message': message})  


@operation.route('/assessment/<assessment_id>', methods=['GET', 'POST'])
def fetch_or_update_assessment(assessment_id):
    if request.method == 'POST':  
        try:
            assessment_form = AssessmentForm(request.form)
            if(not assessment_form.validate()):
                for fieldName, errorMessage in assessment_form.errors.items():
                    raise ValidationError(''+fieldName+' : '+errorMessage[0]+'')

            data = {
                "name": request.form['name'],
                "status": request.form['status'],
                "type": request.form['type'],
                "assessor": request.form['assessor'],
                "created": request.form['created'],
                "lastUpdated": request.form['lastUpdated'],
                "durationInMin": request.form['durationInMin'],
                "security": request.form['security'],
                "invocation": request.form['invocation'],
                "expiry": request.form['expiry'],
                "quesbankType": request.form['quesbankType'],
                "description": request.form['description'],
                "instruction": request.form['instruction']
            }    
            
            update_assessment(data, assessment_id)
            
            return jsonify({
                'status': 'success',
                'message': 'assessment updated successfully'
            })

        except ValidationError as e: 
            message = e.message
            abort(422,{'message': message})     
        
        except KeyError as e:
            message = ''
            abort(400,{'message': message}) 

        except Assessment.DoesNotExist as e:    
            message = 'assessment id doesn\'t exist'
            abort(404,{'message': message})

        except InvalidObjectId as e:
            message = e.message
            abort(404,{'message': message})    

        except Exception as e:
            message = ''
            abort(503,{'message': message})

    try:
        data = fetch_assessment(assessment_id)
        return jsonify({
                'status': 'success',
                'data': data
            })

    except Assessment.DoesNotExist as e:
        message = 'assessment id doesn\'t exist'
        abort(404,{'message': message})  

    except InvalidObjectId as e:
        message = e.message
        abort(404,{'message': message})      

    except Exception as e:
        message = ''
        abort(503,{'message': message})

            