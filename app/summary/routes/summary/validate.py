from wtforms import Form, BooleanField, StringField, validators, IntegerField, SelectField, Field
from ....utils import formValidate, ifValueInEnum,ListField, _validateListLength
from ...constants import *
from ...enumerations import * 

class SummaryInsertForm(Form):
    questionnaireId = Field('questionnaire id', [validators.InputRequired()])
    seekerId = IntegerField('question',[validators.InputRequired()])
    assessedOn = Field('assessedOn',[validators.InputRequired()]) 
    corrects = IntegerField('number of correct answers',[validators.optional(), validators.NumberRange(min=0)])
    wrongs = IntegerField('number of wrong answers',[validators.optional(), validators.NumberRange(min=0)])
    score = IntegerField('total score', [validators.optional()])    
    
def validate(data, action):
    # if action == "update":
    #     formValidate(QuestionUpdateForm, data)
    #     return    

    formValidate(SummaryInsertForm, data)        
