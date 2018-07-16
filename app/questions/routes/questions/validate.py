from wtforms import Form, BooleanField, StringField, validators, IntegerField, SelectField, Field
from ....exception import ValidationError
from ....utils import formValidate, ifValueInEnum,ListField, minListLength
from ...constants import *
from ...enumerations import * 

def validateAnswerOptions(form,field):
    questionType = int(form.type.data)
    if(questionType in (1,2)):
        minListLength(field.data, field.name, 2)    
  
class QuestionInsertForm(Form):
    question = StringField('question',[validators.InputRequired() ])
    type = IntegerField('type of question',[validators.InputRequired(), ifValueInEnum(QuestionType)]) 
    answerOptions = ListField('answer options', [validateAnswerOptions])
    # answer = IntegerField('correct answer',[validators.InputRequired(), validators.NumberRange(min=0)])
    author = IntegerField('id of author', [validators.InputRequired(), validators.NumberRange(min=0)])
    # tags = ListField('tags associated')
    origin = IntegerField('origin',[validators.optional(), ifValueInEnum(QuestionOrigin)])
    level = IntegerField('level',[validators.optional(), ifValueInEnum(QuestionLevel)])

class QuestionUpdateForm(Form):
    question = StringField('question',[validators.InputRequired()]) 
    answerOptions = ListField('answer options', [validateAnswerOptions])
    # tags = ListField('tags associated')
    # answer = IntegerField('correct answer',[validators.InputRequired(), validators.NumberRange(min=0)])
    origin = IntegerField('origin',[validators.optional(), ifValueInEnum(QuestionOrigin)])
    level = IntegerField('level',[validators.optional(), ifValueInEnum(QuestionLevel)])    
    
def validate(data, action):
    if action == "update":
        formValidate(QuestionUpdateForm, data)
        return    

    formValidate(QuestionInsertForm, data)        
