from model import Questionnaire, Question, QuestionResponse
from bson import ObjectId
import bson
from utils import decode_objectId

def associateJobWithQuestionnaire(data, questionnaire_id):
    questionnaire_id = decode_objectId(questionnaire_id)

    if("associationMeta" in data and data["associationMeta"]):
        questionnaire = Questionnaire.objects(id=questionnaire_id).update_one(associationMeta=int(data["associationMeta"]))
    if("associationPublished" in data and data["associationPublished"]):
        questionnaire = Questionnaire.objects(id=questionnaire_id).update_one(associationPublished=int(data["associationPublished"]))    
    if not questionnaire: 
        raise Questionnaire.DoesNotExist

    return

def associatePublishWithMeta(publishId, metaId):
    questionnaire = Questionnaire.objects(associationMeta=int(metaId)).update(associationPublished=int(publishId))
    if not questionnaire:
        return
    setQuestionsAvailability(metaId)
    return    
  
def updateMetaAndPublishAssociation(data):
    if("metaIdOld" in data):
        questionaire = Questionnaire.objects(associationMeta=int(data["metaIdOld"])).update(associationMeta=int(data["metaId"]))
    if("publishIdOld" in data):
        questionaire = Questionnaire.objects(associationPublished=int(data["publishIdOld"])).update(associationPublished=int(data["publishId"]))
        updateQuestionResponseId(data["publishIdOld"], data["publishId"]);
    return

def setQuestionsAvailability(metaId):    
    questionnaire_objects = Questionnaire.objects(associationMeta=int(metaId)).only('sections');

    for questionnaire in questionnaire_objects:
        for section in questionnaire.sections:
            for aQuestionId in section.questionIds:
                Question.objects(id=aQuestionId).update_one(availability=True)

def updateQuestionResponseId(publishIdOld, publishId):
    questionResponse_objects = QuestionResponse.objects(associationPublished=int(publishIdOld)).update(associationPublished=int(publishId));              