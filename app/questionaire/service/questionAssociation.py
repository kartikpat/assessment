from ..model.questionaire import Questionaire
from bson import ObjectId
import bson
from ...exception import InvalidObjectId
from ...utils import is_valid_object_id, decode_objectId
from mongoengine.queryset.visitor import Q

def associate_question_with_questionaire(data, questionaire_id, section_id):
    questionaire_id = decode_objectId(questionaire_id)
    if not is_valid_object_id(questionaire_id):
        raise InvalidObjectId('invalid questionaire id') 

    data["questionIds"] = list(map(decode_objectId, data["questionIds"]))

    questionaire = Questionaire.objects(Q(id=questionaire_id) & Q(sections__id=int(section_id))).update_one(set__sections__S__questionIds= data["questionIds"]);

    if not questionaire:
        raise Questionaire.DoesNotExist

    return


