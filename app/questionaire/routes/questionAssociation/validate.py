from wtforms import Form, validators
from ....exception import ValidationError
from ....utils import ListField, _validateListLength, formValidate
from ...constants import *
from ...enumerations import *   
    
def validate(data):  
    if not "questionIds" in data:
        raise ValidationError("questionIds: This field is required") 
