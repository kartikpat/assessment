from wtforms import Form, BooleanField, StringField, validators, IntegerField, SelectField, Field
from ....exception import ValidationError
from ....utils import formValidate, ifValueInTuple, isIntInstance, ifValueInEnum, isBooleanInstance,ListField, validateListLength, _validateListLength
from ...constants import *
from ...enumerations import * 
from ....enumerations import Invocation


class QuestionaireSectionForm(Form):
    heading = StringField('heading',[validators.optional()])
    type = StringField('type of section',[validators.InputRequired(), ifValueInTuple(questionaireSectionType)]) 
      
      
class QuestionaireInsertForm(Form):
    name = StringField('name',[validators.optional()])
    description = StringField('description',[validators.optional()])
    author = IntegerField('author',[validators.InputRequired()])
    authorType = IntegerField('type of person(recruiter/admin/jobSeeker)',[validators.InputRequired(), ifValueInEnum(AuthorType)]) 
    status = IntegerField('current status of questionaire',[validators.optional(), ifValueInEnum(QuestionaireStatus)]) 
    invocation = IntegerField('stage at which test to be held',[validators.InputRequired(), ifValueInEnum(Invocation)])
    instruction = StringField('instructions if any',[validators.optional()])
    viewType = StringField('view shown to front end user', [validators.optional(), ifValueInTuple(questionaireViewType)])
    blockWindow = Field('block window', [validators.optional(), isBooleanInstance])
    showAnswers = Field('show answers', [validators.optional(), isBooleanInstance])
    durationInMin = IntegerField('test duration', [validators.optional(), validators.NumberRange(min=1)])
    sections = ListField('sections', [_validateListLength])

class QuestionaireUpdateForm(Form):
    description = StringField('description',[validators.optional()]) 
    status = IntegerField('current status of questionaire',[validators.optional(), ifValueInEnum(QuestionaireStatus)]) 
    instruction = StringField('instructions if any',[validators.optional()])
    viewType = StringField('view shown to front end user', [validators.optional(), ifValueInTuple(questionaireViewType)])
    blockWindow = Field('block window', [validators.optional(), isBooleanInstance])
    showAnswers = Field('show answers', [validators.optional(), isBooleanInstance])
    durationInMin = IntegerField('test duration', [validators.optional(), validators.NumberRange(min=1)])  
    sections = ListField('sections', [_validateListLength])  
    
def validate(data, action):
    if action == "update":
        formValidate(QuestionaireUpdateForm, data)  
        sectionValidate(data["sections"])
        return    

    formValidate(QuestionaireInsertForm, data)
    sectionValidate(data["sections"])
    
def sectionValidate(data):
    for index, section in enumerate(data):
        formValidate(QuestionaireSectionForm, section)                
