from app.questions.model.questions import Question
from bson import ObjectId
import bson
from ...exception import InvalidObjectId
from ...utils import is_valid_object_id

def insert_question(data):

    question = Question()
    question.set_data(data)

    question.save()
    question_id = str(question.id)

    return question_id

def update_question(data, question_id):
    if not is_valid_object_id(question_id):
        raise InvalidObjectId('invalid question id') 

    question_o_id = ObjectId(question_id)
    question = Question.objects(id=question_o_id).no_dereference().first()
    if not question:
        raise Question.DoesNotExist

    question.update_data(data)
    question.save()

    return
    
def get_questions_list():
    question_list = []
    for question in Question.objects:
        data = {}

        data = question.get_data(data)

        question_list.append(data)

    return question_list

def get_question(question_id):
    if not is_valid_object_id(question_id):
        raise InvalidObjectId('invalid question id')    

    question_o_id = ObjectId(question_id)
    question = Question.objects(id=question_o_id).no_dereference().first()
    if not question:
        raise Question.DoesNotExist
        
    data = {}
    
    data = question.get_data(data)

    questions_list = []    
    questions_list.append(data)

    return questions_list
