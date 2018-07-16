from wtforms import Form, BooleanField, StringField, validators, IntegerField, SelectField, Field
from ....exception import ValidationError
from ....utils import formValidate, ifValueInEnum, ListField, _validateListLength
from ...constants import *
from ...enumerations import * 

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
        