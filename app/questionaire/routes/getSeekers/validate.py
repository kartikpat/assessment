from wtforms import Form, IntegerField, validators
from ....exception import ValidationError    
    
def validate(data):    
    if not "questions" in data:
        raise ValidationError("questions: This field is required") 
        
        
 