from app.questions.model.questions import Question
from bson import ObjectId
import bson
from ...exception import InvalidObjectId
from ...utils import is_valid_object_id, decode_objectId
from mongoengine.queryset.visitor import Q

def insert_question(data):

    question = Question()
    question.set_data(data)

    question.save()
    question_id = question.id

    return question_id

def update_question(data, question_id):
    question_id = decode_objectId(question_id)
    if not is_valid_object_id(question_id):
        raise InvalidObjectId('invalid question id') 

    question = Question.objects(id=question_id).no_dereference().first()
    if not question:
        raise Question.DoesNotExist

    question.update_data(data)
    question.save()

    return
    
def get_questions(parameters):
    question_list = []

    if parameters["author"]:
        question_objects = Question.objects(Q(author=int(parameters["author"])) & Q(availability=True)).no_dereference() 
    else:
        question_objects = Question.objects

    for question in Question.objects:
        data = {}
        data = question.get_data(data)

        question_list.append(data)

    return question_list

def get_question_by_id(question_id):

    question_id = decode_objectId(question_id)
    if not is_valid_object_id(question_id):
        raise InvalidObjectId('invalid question id')    

    question = Question.objects(id=question_id).no_dereference().first()
    if not question:
        raise Question.DoesNotExist
        
    data = {}
    
    data = question.get_data(data)

    return data
