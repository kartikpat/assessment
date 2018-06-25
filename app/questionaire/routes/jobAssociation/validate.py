from wtforms import Form
from ....exception import ValidationError
from ....utils import ListField, _validateListLength, formValidate
from ...constants import *
from ...enumerations import * 

class jobAssociateForm(Form):
    jobs = ListField('jobs associated', [_validateListLength])    
    
def validate(data):    
    formValidate(jobAssociateForm, data)
        
        
 