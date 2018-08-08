from wtforms import Form, IntegerField, validators
from ....utils import formValidate

class jobAssociateForm(Form):
    associationMeta = IntegerField('associationMeta',[validators.optional()]) 
    associationPublished = IntegerField('associationPublished',[validators.optional()])
    
def validate(data):    
    formValidate(jobAssociateForm, data)
        
        
 