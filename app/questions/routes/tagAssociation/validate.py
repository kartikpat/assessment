from wtforms import Form, BooleanField, StringField, validators, IntegerField, SelectField, Field
from app.exception import ValidationError
from app.utils import get_multiDict_data, isStringInstance, ifValueInEnum,ListField, _validateListLength
from app.questions.constants import *
from app.questions.enumerations import * 

class tagAssociateForm(Form):
    tags = ListField('tags associated', [_validateListLength])    
    
def validate(data):    
    formValidate(tagAssociateForm, data)
        
def formValidate(form_name, data):    
    mdict_data = get_multiDict_data(data)
    form_name = form_name(mdict_data)
    if not form_name.validate():
        for fieldName, errorMessage in form_name.errors.items():
            raise ValidationError(''+fieldName+' : '+errorMessage[0]+'')        
 