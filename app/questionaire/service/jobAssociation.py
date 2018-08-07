from ..model.questionaire import Questionaire
from bson import ObjectId
import bson
from ...exception import InvalidObjectId
from ...utils import is_valid_object_id

def associateJobWithquestionaire(data, questionaire_id):
    questionaire_id = decode_objectId(questionaire_id)
    if not is_valid_object_id(questionaire_id):
        raise InvalidObjectId('invalid questionaire id') 

    if("associationMeta" in data and data["associationMeta"]):
        questionaire = Questionaire.objects(id=questionaire_id).update_one(associationMeta=data["associationMeta"])
    if("associationPublished" in data and data["associationPublished"]):
        questionaire = Questionaire.objects(id=questionaire_id).update_one(associationPublished=data["associationPublished"])    
    if not questionaire: 
        raise Questionaire.DoesNotExist

    return
    
def getAssociatedJobWithQuestionaire(questionaire_id):
    questionaire_id = decode_objectId(questionaire_id)
    if not is_valid_object_id(questionaire_id):
        raise InvalidObjectId('invalid questionaire id')    

    questionaire = Questionaire.objects(id=questionaire_id).only('associationPublished','associationMeta').first()
    data = {}

    if("associationMeta" in questionaire):
        data["associationMeta"] = questionaire.associationMeta;
    if("associationPublished" in questionaire):
        data["associationPublished"] = questionaire.associationPublished;

    return data
