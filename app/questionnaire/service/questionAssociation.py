from ..model.questionnaire import Questionnaire
from bson import ObjectId
import bson
from ...exception import InvalidObjectId
from ...utils import is_valid_object_id, decode_objectId
from mongoengine.queryset.visitor import Q

# def checkIfQuestionAssociatedWithMultipleQuestionnaire(question_id):
#     question_id = decode_objectId(question_id)
#     if not is_valid_object_id(question_id):
#         raise InvalidObjectId('invalid question id')
        
#     questionnaire = Questionnaire.objects(sections__questionIds=question_id).count();
#     if questionnaire > 1:
#         return True
#     return False    

def associate_question_with_questionnaire(data, questionnaire_id, section_id):
    questionnaire_id = decode_objectId(questionnaire_id)
    if not is_valid_object_id(questionnaire_id):
        raise InvalidObjectId('invalid questionnaire id') 

    data["questionIds"] = list(map(decode_objectId, data["questionIds"]))

    questionnaire = Questionnaire.objects(Q(id=questionnaire_id) & Q(sections__id=int(section_id))).update_one(set__sections__S__questionIds= data["questionIds"]);

    if not questionnaire:
        raise Questionnaire.DoesNotExist

    return


