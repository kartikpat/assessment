from wtforms import Form, IntegerField, validators
from ....exception import FormValidationError    
    
def validate(data):    
    if not "questions" in data:
        raise FormValidationError("questions: This field is required") 
        
        
 