from wtforms import Form, BooleanField, StringField, validators, IntegerField, SelectField, Field
from app.exception import ValidationError
from app.utils import get_multiDict_data, isStringInstance, ifValueInEnum,ListField, _validateListLength
from app.questions.constants import *
from app.questions.enumerations import * 

class QuestionInsertForm(Form):
    question = StringField('question',[validators.InputRequired(), isStringInstance])
    type = IntegerField('type of question',[validators.InputRequired(), ifValueInEnum(QuestionType)]) 
    ansOptions = ListField('answer options', [_validateListLength])
    answer = IntegerField('correct answer',[validators.InputRequired(), validators.NumberRange(min=0)])
    createdBy = IntegerField('id of author', [validators.InputRequired(), validators.NumberRange(min=0)])
    tags = ListField('tags associated')
    origin = IntegerField('origin',[validators.optional(), ifValueInEnum(QuestionOrigin)])
    level = IntegerField('level',[validators.optional(), ifValueInEnum(QuestionLevel)])

class QuestionUpdateForm(Form):
    question = StringField('question',[validators.InputRequired(), isStringInstance]) 
    ansOptions = ListField('answer options', [_validateListLength])
    tags = ListField('tags associated')
    answer = IntegerField('correct answer',[validators.InputRequired(), validators.NumberRange(min=0)])
    level = IntegerField('level',[validators.optional(), ifValueInEnum(QuestionLevel)])    
    
def validate(data, action):
    if action == "update":
        formValidate(QuestionUpdateForm, data)
        return    

    formValidate(QuestionInsertForm, data)
        
def formValidate(form_name, data):    
    mdict_data = get_multiDict_data(data)
    form_name = form_name(mdict_data)
    if not form_name.validate():
        for fieldName, errorMessage in form_name.errors.items():
            raise ValidationError(''+fieldName+' : '+errorMessage[0]+'')        
