from wtforms import Form, IntegerField, validators
from ....exception import ValidationError
from ....utils import formValidate
from ...constants import *
from ...enumerations import * 

class jobAssociateForm(Form):
    associationMeta = IntegerField('associationMeta',[validators.optional()]) 
    associationPublished = IntegerField('associationPublished',[validators.optional()])
    
def validate(data):    
    formValidate(jobAssociateForm, data)
        
        
 