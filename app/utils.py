import time
from flask import request
from werkzeug.datastructures import MultiDict
from .exception import BadContentType, ValidationError
from bson import ObjectId
import bson
import dateutil.parser as parser
from wtforms import Form, Field
from flask import current_app

def timestamp():
    """Return the current timestamp as an integer."""
    return int(time.time())

def get_multiDict_data(data):
    mdict_data = MultiDict(mapping=data)
    return mdict_data


def is_valid_object_id(object_id):
    if not bson.objectid.ObjectId.is_valid(object_id):
        return False

    return True 

def get_data_in_dict():  
    if request.is_json:
        data = request.get_json()
        return data
    
    elif request.form:
        data = request.form.to_dict()
        return data

    raise BadContentType('content type is not valid')

def isStringInstance(form,field):
    if not isinstance(field.data, str):
        raise ValidationError(field.name + " : " + "only string values are accepted")  

def isIntInstance(form,field):
    if not isinstance(field.data, int):
        raise ValidationError(field.name + " : " + "only int values are accepted")  

def ifValueInTuple(tuple_name, message=None):
    if not message:
        message = 'not a valid choice'
    def _ifValueInTuple(form, field):
        value = field.data
        if not value in tuple_name:
            raise ValidationError(field.name + " : " + message)

    return _ifValueInTuple            

def ifValueInEnum(enum_name, message=None):
    if not message:
        message = 'not a valid choice'
    def _ifValueInEnum(form, field):
        value = field.data
        if not any(value == item.value for item in enum_name):
            raise ValidationError(field.name + " : " + message)

    return _ifValueInEnum

def isBooleanInstance(form, field):
    if not field.data in (True,False,0,1):
        raise ValidationError(field.name + " : " + "only boolean values are accepted")

def getBooleanValue(val):
    return bool(val) 

def getDateInIsoFormat(date):
    return (parser.parse(str(date))).isoformat()

class ListField(Field):
    def process_formdata(self, valuelist):
        self.data = valuelist 

def _validateListLength(form, field):
    validateListLength(field.data, field.name)

def validateListLength(list_data, list_name):
    if len(list_data) == 0:
        raise ValidationError(list_name + ' list can\'t be empty')        

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config.get('ALLOWED_EXTENSIONS')
        

# def requiredIfFieldExist(field_name, field_value):
#     def _requiredIfFieldExist(form, field):
#         if(form[field_name].data == field_value):
#             print(form[field_name].data)
#             value = field.data
#             if not value:
#                 raise ValidationError(field.name + " : " + "field is required" )

#     return _requiredIfFieldExist
                               

# class RequiredIf(Required):
#     # a validator which makes a field required if
#     # another field is set and has a truthy value

#     def __init__(self, other_field_name, *args, **kwargs):
#         self.other_field_name = other_field_name
#         super(RequiredIf, self).__init__(*args, **kwargs)

#     def __call__(self, form, field):
#         other_field = form._fields.get(self.other_field_name)
#         if other_field is None:
#             raise Exception('no field named "%s" in form' % self.other_field_name)
#         if bool(other_field.data):
#             super(RequiredIf, self).__call__(form, field)    