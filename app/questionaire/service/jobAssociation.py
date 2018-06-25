from ..model.questionaire import Questionaire
from bson import ObjectId
import bson
from ...exception import InvalidObjectId
from ...utils import is_valid_object_id

def associate_job_list_with_questionaire(data, questionaire_id):
    if not is_valid_object_id(questionaire_id):
        raise InvalidObjectId('invalid questionaire id') 

    questionaire_o_id = ObjectId(questionaire_id)

    questionaire = Questionaire.objects(id=questionaire_o_id).update_one(_tags=data["tags"])
    if not questionaire:
        raise Questionaire.DoesNotExist

    return
    
def get_associated_job_list_with_questionaire(questionaire_id):
    if not is_valid_object_id(questionaire_id):
        raise InvalidObjectId('invalid questionaire id')    

    questionaire_o_id = ObjectId(questionaire_id)
    questionaire = Questionaire.objects(id=questionaire_o_id).only('_tags').first()
    data = {}

    data["tags"] = questionaire._tags
    tags_list = []    
    tags_list.append(data)

    return tags_list
