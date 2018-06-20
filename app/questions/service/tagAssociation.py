from app.questions.model.questions import Question
from bson import ObjectId
import bson
from app.exception import InvalidObjectId
from app.utils import is_valid_object_id

def update_tags_with_question(data, question_id):
    if not is_valid_object_id(question_id):
        raise InvalidObjectId('invalid question id') 

    question_o_id = ObjectId(question_id)

    question = Question.objects(id=question_o_id).update_one(_tags=data["tags"])
    if not question:
        raise Question.DoesNotExist

    return
    
def get_associated_tags_with_question(question_id):
    if not is_valid_object_id(question_id):
        raise InvalidObjectId('invalid question id')    

    question_o_id = ObjectId(question_id)
    question = Question.objects(id=question_o_id).only('_tags').first()
    data = {}

    data["tags"] = question._tags
    tags_list = []    
    tags_list.append(data)

    return tags_list
