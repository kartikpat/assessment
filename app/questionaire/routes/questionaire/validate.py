from wtforms import Form, BooleanField, StringField, validators, IntegerField, SelectField, Field
from app.exception import ValidationError
from app.utils import get_multiDict_data, isStringInstance, ifValueInTuple, isIntInstance, ifValueInEnum, isBooleanInstance,ListField, validateListLength, _validateListLength
from app.questionaire.constants import *
from app.questionaire.enumerations import * 

class QuestionsListField(ListField):
    def pre_validate(self, form):
        if(form.type.data == "static"):
            validateListLength(self.data, self.name)

class TagsListField(ListField):
    def pre_validate(self, form):
        if(form.type.data == "dynamic"):
            validateListLength(self.data, self.name) 

def validateNoOfQuestionField(form, field):
    if form.type.data == "dynamic":
        if not field.data:
            raise ValidationError(field.name + " : " + "field is required" )
        isIntInstance(form, field)
        if field.data <= 0:
            raise ValidationError(field.name + " : " + "value should be atleast one")

class QuestionareSectionForm(Form):
    heading = StringField('heading',[validators.optional(), isStringInstance])
    type = StringField('type of section',[validators.InputRequired(), ifValueInTuple(questionaireSectionType)]) 
    questions = QuestionsListField('static question ids associated with questionaire')
    tags = TagsListField('tag ids for dynamic questionaire')  
    noOfQuestion = Field('number of questions for dynamic questionaire', [validateNoOfQuestionField])

class QuestionaireInsertForm(Form):
    name = StringField('name',[validators.InputRequired(), isStringInstance])
    description = StringField('description',[validators.optional(), isStringInstance])
    author = IntegerField('id of the person created by',[validators.InputRequired(), validators.NumberRange(min=1)])
    authorType = IntegerField('type of person(recruiter/admin/jobSeeker)',[validators.InputRequired(), ifValueInEnum(AuthorType)]) 
    status = IntegerField('current status of questionaire',[validators.optional(), ifValueInEnum(QuestionaireStatus)]) 
    invocation = IntegerField('stage at which test to be held',[validators.optional(), ifValueInEnum(QuestionaireInvocation)])
    instruction = StringField('instructions if any',[validators.optional(), isStringInstance])
    viewType = StringField('view shown to front end user', [validators.optional(), ifValueInTuple(questionaireViewType)])
    blockWindow = Field('block window', [validators.optional(), isBooleanInstance])
    showAnswers = Field('show answers', [validators.optional(), isBooleanInstance])
    durationInMin = IntegerField('test duration', [validators.optional(), validators.NumberRange(min=1)])
    sections = ListField('sections', [_validateListLength])

class QuestionaireUpdateForm(Form):
    description = StringField('description',[validators.optional(), isStringInstance]) 
    status = IntegerField('current status of questionaire',[validators.optional(), ifValueInEnum(QuestionaireStatus)]) 
    invocation = IntegerField('stage at which test to be held',[validators.optional(), ifValueInEnum(QuestionaireInvocation)])
    instruction = StringField('instructions if any',[validators.optional(), isStringInstance])
    viewType = StringField('view shown to front end user', [validators.optional(), ifValueInTuple(questionaireViewType)])
    blockWindow = Field('block window', [validators.optional(), isBooleanInstance])
    showAnswers = Field('show answers', [validators.optional(), isBooleanInstance])
    durationInMin = IntegerField('test duration', [validators.optional(), validators.NumberRange(min=1)])    
    
def validate(data, action):
    if action == "update":
        formValidate(QuestionaireUpdateForm, data)  
        if len(data["sections"]) > 0:
            sectionValidate(data["sections"])
        return    

    formValidate(QuestionaireInsertForm, data)
    sectionValidate(data["sections"])
    
def sectionValidate(data):
    for index, section in enumerate(data):
        formValidate(QuestionareSectionForm, section)        
        
def formValidate(form_name, data):    
    mdict_data = get_multiDict_data(data)
    form_name = form_name(mdict_data)
    if not form_name.validate():
        for fieldName, errorMessage in form_name.errors.items():
            raise ValidationError(''+fieldName+' : '+errorMessage[0]+'')        
