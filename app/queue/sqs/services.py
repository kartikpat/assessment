from model import Questionnaire, Question
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
    setQuestionsAvailability(metaId)
    return    
  
def updateMetaAndPublishAssociation(data):
    if("metaIdOld" in data):
        questionaire = Questionnaire.objects(associationMeta=data["metaIdOld"]).update(associationMeta=int(data["metaId"]))
    if("publishIdOld" in data):
        questionaire = Questionnaire.objects(associationPublished=data["publishIdOld"]).update(associationPublished=int(data["publishId"]))
    return


def setQuestionsAvailability(metaId):    
    questionnaire_objects = Questionnaire.objects(associationMeta=metaId).only('sections');

    for questionnaire in questionnaire_objects:
        for section in questionnaire.sections:
            for aQuestionId in section.questionIds:
                Question.objects(id=aQuestionId).update_one(availability=True)