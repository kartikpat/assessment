from wtforms import Form, BooleanField, StringField, validators, IntegerField, SelectField, Field
from ....utils import formValidate, ifValueInTuple, isIntInstance, ifValueInEnum, isBooleanInstance,ListField, validateListLength, _validateListLength
from ...constants import *
from ...enumerations import * 
from ....enumerations import Invocation


class QuestionnaireSectionForm(Form):
    heading = StringField('heading',[validators.optional()])
    type = StringField('type of section',[validators.InputRequired(), ifValueInTuple(questionnaireSectionType)]) 
      
      
class QuestionnaireInsertForm(Form):
    name = StringField('name',[validators.optional()])
    description = StringField('description',[validators.optional()])
    author = IntegerField('author',[validators.InputRequired()])
    authorType = IntegerField('type of person(recruiter/admin/jobSeeker)',[validators.InputRequired(), ifValueInEnum(AuthorType)]) 
    status = IntegerField('current status of questionnaire',[validators.optional(), ifValueInEnum(QuestionnaireStatus)]) 
    invocation = IntegerField('stage at which test to be held',[validators.InputRequired(), ifValueInEnum(Invocation)])
    instruction = StringField('instructions if any',[validators.optional()])
    viewType = StringField('view shown to front end user', [validators.optional(), ifValueInTuple(questionnaireViewType)])
    blockWindow = Field('block window', [validators.optional(), isBooleanInstance])
    showAnswers = Field('show answers', [validators.optional(), isBooleanInstance])
    durationInMin = IntegerField('test duration', [validators.optional(), validators.NumberRange(min=1)])
    sections = ListField('sections', [_validateListLength])

class QuestionnaireUpdateForm(Form):
    description = StringField('description',[validators.optional()]) 
    status = IntegerField('current status of questionnaire',[validators.optional(), ifValueInEnum(QuestionnaireStatus)]) 
    instruction = StringField('instructions if any',[validators.optional()])
    viewType = StringField('view shown to front end user', [validators.optional(), ifValueInTuple(questionnaireViewType)])
    blockWindow = Field('block window', [validators.optional(), isBooleanInstance])
    showAnswers = Field('show answers', [validators.optional(), isBooleanInstance])
    durationInMin = IntegerField('test duration', [validators.optional(), validators.NumberRange(min=1)])  
    sections = ListField('sections', [_validateListLength])  
    
def validate(data, action):
    if action == "update":
        formValidate(QuestionnaireUpdateForm, data)  
        sectionValidate(data["sections"])
        return    

    formValidate(QuestionnaireInsertForm, data)
    sectionValidate(data["sections"])
    
def sectionValidate(data):
    for index, section in enumerate(data):
        formValidate(QuestionnaireSectionForm, section)                
