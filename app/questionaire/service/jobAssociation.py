from ..model.questionaire import Questionaire
from bson import ObjectId
import bson
from ...exception import InvalidObjectId
from ...utils import is_valid_object_id, decode_objectId

def associateJobWithQuestionaire(data, questionaire_id):
    questionaire_id = decode_objectId(questionaire_id)
    if not is_valid_object_id(questionaire_id):
        raise InvalidObjectId('invalid questionaire id') 

    if("associationMeta" in data and data["associationMeta"]):
        questionaire = Questionaire.objects(id=questionaire_id).update_one(associationMeta=int(data["associationMeta"]))
    if("associationPublished" in data and data["associationPublished"]): 
        questionaire = Questionaire.objects(id=questionaire_id).update_one(associationPublished=int(data["associationPublished"]))

    if not questionaire:
        raise Questionaire.DoesNotExist

    return

def associatePublishWithMeta(publishId, metaId):
    questionaire = Questionaire.objects(associationMeta=metaId).update(associationPublished=int(publishId))
    return    
  
def updateMetaAndPublishAssociation(data):
    if("metaIdOld" in data):
        questionaire = Questionaire.objects(associationMeta=data["metaIdOld"]).update(associationMeta=int(data["metaId"]))
    if("publishIdOld" in data):
        questionaire = Questionaire.objects(associationPublished=data["publishIdOld"]).update(associationPublished=int(data["publishId"]))
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
