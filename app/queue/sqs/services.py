from model import Questionnaire
from bson import ObjectId
import bson
from utils import decode_objectId

def associateJobWithQuestionnaire(data, questionnaire_id):
    questionnaire_id = decode_objectId(questionnaire_id)

    if("associationMeta" in data and data["associationMeta"]):
        questionnaire = Questionnaire.objects(id=questionnaire_id).update_one(associationMeta=data["associationMeta"])
    if("associationPublished" in data and data["associationPublished"]):
        questionnaire = Questionnaire.objects(id=questionnaire_id).update_one(associationPublished=data["associationPublished"])    
    if not questionnaire: 
        raise Questionnaire.DoesNotExist

    return

def associatePublishWithMeta(publishId, metaId):
    questionaire = Questionnaire.objects(associationMeta=metaId).update(associationPublished=int(publishId))
    return    
  
def updateMetaAndPublishAssociation(data):
    if("metaIdOld" in data):
        questionaire = Questionnaire.objects(associationMeta=data["metaIdOld"]).update(associationMeta=int(data["metaId"]))
    if("publishIdOld" in data):
        questionaire = Questionnaire.objects(associationPublished=data["publishIdOld"]).update(associationPublished=int(data["publishId"]))
    return 