from ..model.questionnaire import Questionaire
from bson import ObjectId
import bson
from ...exception import InvalidObjectId
from ...utils import is_valid_object_id

def associateJobWithquestionnaire(data, questionnaire_id):
    questionnaire_id = decode_objectId(questionnaire_id)
    if not is_valid_object_id(questionnaire_id):
        raise InvalidObjectId('invalid questionnaire id') 

    if("associationMeta" in data and data["associationMeta"]):
        questionnaire = Questionaire.objects(id=questionnaire_id).update_one(associationMeta=data["associationMeta"])
    if("associationPublished" in data and data["associationPublished"]):
        questionnaire = Questionaire.objects(id=questionnaire_id).update_one(associationPublished=data["associationPublished"])    
    if not questionnaire: 
        raise Questionaire.DoesNotExist

    return
    
def getAssociatedJobWithQuestionaire(questionnaire_id):
    questionnaire_id = decode_objectId(questionnaire_id)
    if not is_valid_object_id(questionnaire_id):
        raise InvalidObjectId('invalid questionnaire id')    

    questionnaire = Questionaire.objects(id=questionnaire_id).only('associationPublished','associationMeta').first()
    data = {}

    if("associationMeta" in questionnaire):
        data["associationMeta"] = questionnaire.associationMeta;
    if("associationPublished" in questionnaire):
        data["associationPublished"] = questionnaire.associationPublished;

    return data
