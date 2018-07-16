from wtforms import Form, BooleanField, StringField, validators, IntegerField, SelectField, Field
from ....exception import ValidationError
from ....utils import formValidate, ifValueInTuple, isIntInstance, ifValueInEnum, isBooleanInstance,ListField, validateListLength, _validateListLength
from ...constants import *
from ...enumerations import * 

# class QuestionsListField(ListField):
#     def pre_validate(self, form):
#         if(form.type.data == "static"):
#             validateListLength(self.data, self.name)

# class TagsListField(ListField):
#     def pre_validate(self, form):
#         if(form.type.data == "dynamic"):
#             validateListLength(self.data, self.name) 

# def validateNoOfQuestionField(form, field):
#     if form.type.data == "dynamic":
#         if not field.data:
#             raise ValidationError(field.name + " : " + "field is required" )
#         isIntInstance(form, field)
#         if field.data <= 0:
#             raise ValidationError(field.name + " : " + "value should be atleast one")

class QuestionareSectionForm(Form):
    heading = StringField('heading',[validators.optional()])
    type = StringField('type of section',[validators.InputRequired(), ifValueInTuple(questionaireSectionType)]) 
      
      
class QuestionaireInsertForm(Form):
    name = StringField('name',[validators.optional()])
    description = StringField('description',[validators.optional()])
    author = IntegerField('author',[validators.InputRequired()])
    association = IntegerField('association',[validators.optional()])
    authorType = IntegerField('type of person(recruiter/admin/jobSeeker)',[validators.InputRequired(), ifValueInEnum(AuthorType)]) 
    status = IntegerField('current status of questionaire',[validators.optional(), ifValueInEnum(QuestionaireStatus)]) 
    invocation = IntegerField('stage at which test to be held',[validators.InputRequired(), ifValueInEnum(QuestionaireInvocation)])
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
        formValidate(QuestionareSectionForm, section)                
