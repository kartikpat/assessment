from wtforms import Form, validators
from ....exception import FormValidationError
from ....utils import ListField, _validateListLength, formValidate
from ...constants import *
from ...enumerations import *   
    
def validate(data):  
    if not "questionIds" in data:
        raise FormValidationError("questionIds: This field is required") 
