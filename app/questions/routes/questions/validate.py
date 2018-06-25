from wtforms import Form, BooleanField, StringField, validators, IntegerField, SelectField, Field
from ....exception import ValidationError
from ....utils import formValidate, isStringInstance, ifValueInEnum,ListField, _validateListLength
from ...constants import *
from ...enumerations import * 

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
