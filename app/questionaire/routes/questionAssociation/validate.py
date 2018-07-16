from wtforms import Form, validators
from ....exception import ValidationError
from ....utils import ListField, _validateListLength, formValidate
from ...constants import *
from ...enumerations import * 

# class questionAssociateForm(Form):
#     questionIds = ListField('questions associated', [keyRequired])    
    
def validate(data):  
    if not "questionIds" in data:
        raise ValidationError("questionIds: This field is required") 
    # formValidate(questionAssociateForm, data)