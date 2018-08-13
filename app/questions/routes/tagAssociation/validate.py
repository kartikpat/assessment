from wtforms import Form, BooleanField, StringField, validators, IntegerField, SelectField, Field
from ....utils import formValidate, ifValueInEnum,ListField, _validateListLength
from ...constants import *
from ...enumerations import * 

class tagAssociateForm(Form):
    tags = ListField('tags associated', [_validateListLength])    
    
def validate(data):    
    formValidate(tagAssociateForm, data)
                
 