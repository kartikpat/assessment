from wtforms import Form, BooleanField, StringField, validators, IntegerField, SelectField, Field
from app.exception import ValidationError
from app.utils import get_multiDict_data, isStringInstance, ifValueInEnum, ListField, _validateListLength
from app.questionResponse.constants import *
from app.questionResponse.enumerations import * 

class QuestionResponseInsertForm(Form):
    questionId = Field('question id', [validators.InputRequired()])
    questionaireId = Field('questionaire id', [validators.InputRequired()])
    seekerId = IntegerField('question',[validators.InputRequired()])
    assessedOn = Field('assessedOn',[validators.InputRequired()]) 
    timeTaken = IntegerField('total time taken',[validators.optional()])   
    
def validate(data, action):
    # if action == "update":
    #     formValidate(QuestionUpdateForm, data)
    #     return    

    formValidate(QuestionResponseInsertForm, data)
        
def formValidate(form_name, data):    
    mdict_data = get_multiDict_data(data)
    form_name = form_name(mdict_data)
    if not form_name.validate():
        for fieldName, errorMessage in form_name.errors.items():
            raise ValidationError(''+fieldName+' : '+errorMessage[0]+'') 