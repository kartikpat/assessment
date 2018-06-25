from app.questionResponse.model.questionResponse import QuestionResponse
from bson import ObjectId
import bson
from ...exception import InvalidObjectId
from ...utils import is_valid_object_id, decode_objectId

def insert_questionResponse(data):

    questionResponse = QuestionResponse()
    questionResponse.set_data(data)

    questionResponse.save()
    questionResponse_id = str(questionResponse.id)

    return questionResponse_id

def update_questionResponse(data, questionResponse_id):
    questionResponse_id = decode_objectId(questionResponse_id)

    if not is_valid_object_id(questionResponse_id):
        raise InvalidObjectId('invalid questionResponse id') 

    questionResponse_o_id = ObjectId(questionResponse_id)
    questionResponse = QuestionResponse.objects(id=questionResponse_o_id).no_dereference().first()
    if not questionResponse:
        raise QuestionResponse.DoesNotExist

    questionResponse.update_data(data)
    questionResponse.save()

    return
    
def get_questionResponse_list():
    questionResponse_list = []
    for questionResponse in QuestionResponse.objects:
        data = {}

        data = questionResponse.get_data(data)

        questionResponse_list.append(data)

    return questionResponse_list

def get_questionResponse(questionResponse_id):
    questionResponse_id = decode_objectId(questionResponse_id)
    
    if not is_valid_object_id(questionResponse_id):
        raise InvalidObjectId('invalid questionResponse id')    

    questionResponse_o_id = ObjectId(questionResponse_id)
    questionResponse = QuestionResponse.objects(id=questionResponse_o_id).no_dereference().first()
    if not questionResponse:
        raise QuestionResponse.DoesNotExist    

    data = {}
    
    data = questionResponse.get_data(data)

    questionResponse_list = []    
    questionResponse_list.append(data)

    return questionResponse_list
