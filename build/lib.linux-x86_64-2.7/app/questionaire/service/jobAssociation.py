from ..model.questionaire import Questionaire
from bson import ObjectId
import bson
from ...exception import InvalidObjectId
from ...utils import is_valid_object_id

def associate_job_list_with_questionaire(data, questionaire_id):
    questionaire_id = decode_objectId(questionaire_id)
    if not is_valid_object_id(questionaire_id):
        raise InvalidObjectId('invalid questionaire id') 

    questionaire = Questionaire.objects(id=questionaire_id).update_one(associationMeta=data["associationMeta"])
    if not questionaire:
        raise Questionaire.DoesNotExist

    return
    
def get_associated_job_list_with_questionaire(questionaire_id):
    questionaire_id = decode_objectId(questionaire_id)
    if not is_valid_object_id(questionaire_id):
        raise InvalidObjectId('invalid questionaire id')    

    questionaire = Questionaire.objects(id=questionaire_id).only('tags').first()
    data = {}

    data["tags"] = questionaire.tags
    tags_list = []    
    tags_list.append(data)

    return tags_list
