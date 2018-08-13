from wtforms import Form, IntegerField, validators
from ....exception import FormValidationError    
from ....utils import formValidate, ifValueInTuple, _validateListLength, ListField

class SeekerResponseForm(Form):
    invocation = IntegerField('heading',[validators.InputRequired()])
      
class SeekerForm(Form):
    questionnaire = ListField('questionnaire',[_validateListLength])
    associationPublished = IntegerField('description',[validators.InputRequired()])
    
def validate(data):    
    if not "questionnaire" in data:
        raise FormValidationError("questionnaire: This field is required") 
    if not "associationPublished" in data:    
        raise FormValidationError("associationPublished: This field is required")


def validate(data):
    formValidate(SeekerForm, data)
    sectionValidate(data["questionnaire"])
    
def sectionValidate(data):
    for index, section in enumerate(data):
        formValidate(SeekerResponseForm, section)
        if not "questions" in section:
        	raise FormValidationError("questions: This field is required")
        
 