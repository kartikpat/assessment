from wtforms import Form, IntegerField, validators
from ....exception import ValidationError
from ....utils import formValidate
from ...constants import *
from ...enumerations import * 

class jobAssociateForm(Form):
    association = IntegerField('association',[validators.InputRequired()])    
    
def validate(data):    
    formValidate(jobAssociateForm, data)
        
        
 