from wtforms import Form, BooleanField, StringField, validators, IntegerField, SelectField, Field
from ....exception import ValidationError
from ....utils import formValidate, ifValueInEnum, ListField, _validateListLength
from ...constants import *
from ...enumerations import * 
from ....enumerations import Invocation

class QuestionResponseSectionForm(Form):
    id = StringField('heading',[validators.optional()])
    questions = ListField('question details', [_validateListLength]) 

class QuestionResponseInsertForm(Form):
    sections = ListField('sections', [_validateListLength])
    questionaireId = Field('questionaire id', [validators.InputRequired()])
    invocation = IntegerField('stage at which test to be held',[validators.InputRequired(), ifValueInEnum(Invocation)])
    seeker = IntegerField('job seeker id',[validators.InputRequired()])
    assessedOn = Field('assessedOn',[validators.InputRequired()]) 
    timeTaken = IntegerField('total time taken',[validators.optional()])  
    associationPublished = IntegerField('associationPublished',[validators.InputRequired()]) 
    
def validate(data, action):
    # if action == "update":
    #     formValidate(QuestionUpdateForm, data)
    #     return    

    formValidate(QuestionResponseInsertForm, data)
    sectionValidate(data["sections"])
    
def sectionValidate(data):
    for index, section in enumerate(data):
        formValidate(QuestionResponseSectionForm, section)
        