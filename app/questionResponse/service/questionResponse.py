from app.questionResponse.model.questionResponse import QuestionResponse, QuestionDetail, QuestionResponseSection
from app.questionnaire.model.questionnaire import Questionaire
from bson import ObjectId
import bson
from ...exception import InvalidObjectId, EntityNotExists
from ...utils import is_valid_object_id, decode_objectId, encode_objectId
from mongoengine.queryset.visitor import Q
import app.questions.service as question_service_module
import app.questionnaire.service as questionnaire_service_module 

def questionResponse_exist(data):
    questionResponse = QuestionResponse.objects(Q(associationPublished=data["associationPublished"]) & Q(invocation=int(data["invocation"])) & Q(seeker=int(data["seeker"]))).only('id').first()
    if questionResponse:
       return questionResponse.id

def getQuestionResponse(data, seeker, associationPublished,invocation, questionId, sectionId):
    if(invocation):
        pipeline = [
                {"$match": {"associationPublished": int(associationPublished), "invocation": int(invocation), "seeker": int(seeker)}},
                {"$project": {"sections":1, "_id":0}},
                {"$unwind": "$sections"},
                {"$match": {"sections.id": sectionId}},
                {"$project": {"sections.questions":1}},
                {"$unwind": "$sections.questions"},
                {"$match": {"sections.questions.id": questionId}},
                {"$project": {"sections.questions.answer": 1}}
               ]

    else:
        pipeline = [
                    {"$match": {"associationPublished": int(associationPublished), "seeker": int(seeker)}},
                    {"$project": {"sections":1, "_id":0}},
                    {"$unwind": "$sections"},
                    {"$match": {"sections.id": sectionId}},
                    {"$project": {"sections.questions":1}},
                    {"$unwind": "$sections.questions"},
                    {"$match": {"sections.questions.id": questionId}},
                    {"$project": {"sections.questions.answer": 1}}
                   ]

    questionResponse = QuestionResponse.objects.aggregate(*pipeline)
    for aQuestionResponse in questionResponse:
        data["answer"] = aQuestionResponse["sections"]["questions"]["answer"];

    return data    

def insert_questionResponse(data):
    questionnaireExistParameters = {
        "associationPublished": data["associationPublished"],
        "invocation": data["invocation"]
    }

    questionnaireId = questionnaire_service_module.questionnaire.questionnaire_exist(questionnaireExistParameters);

    if not questionnaireId:
        raise EntityNotExists('no questionnaire is associated with the job')   

    sections = createQuestionResponseSections(data)

    questionResponse = QuestionResponse()
    questionResponse.set_data(data, sections)

    questionResponse.save()
    questionResponse_id = questionResponse.id

    return questionResponse_id

def update_questionResponse(data, questionResponse_id):
    questionResponse_id = decode_objectId(questionResponse_id)
    if not is_valid_object_id(questionResponse_id):
        raise InvalidObjectId('invalid questionResponse id') 

    questionResponse = QuestionResponse.objects(id=questionResponse_id).no_dereference().first()
    if not questionResponse:
        raise QuestionResponse.DoesNotExist

    sections = createQuestionResponseSections(data)    

    questionResponse.set_data(data, sections)
    questionResponse.save()

    return
    
def get_questionResponse_list(parameters):
    questionResponse_list = []

    if parameters["seeker"] and parameters["invocation"] and parameters["associationPublished"]:
        questionResponse_objects = QuestionResponse.objects(Q(associationPublished=int(parameters["associationPublished"])) & Q(invocation=int(parameters["invocation"])) & Q(seeker=int(parameters["seeker"]))).no_dereference() 
    else:
        questionResponse_objects = QuestionResponse.objects

    if not len(questionResponse_objects): 
        return questionResponse_list
    
    for questionResponse in questionResponse_objects:
        data = {}

        data = questionResponse.get_data(data)

        data = getSectionData(questionResponse, data)

        questionResponse_list.append(data)

    return questionResponse_list

def get_questionResponse(questionResponse_id):
    questionResponse_id = decode_objectId(questionResponse_id)    
    if not is_valid_object_id(questionResponse_id):
        raise InvalidObjectId('invalid questionResponse id')    

    questionResponse = QuestionResponse.objects(id=questionResponse_id).no_dereference().first()
    if not questionResponse:
        raise QuestionResponse.DoesNotExist    

    data = {}
    
    data = questionResponse.get_data(data)

    data = getSectionData(questionResponse, data)

    questionResponse_list = []    
    questionResponse_list.append(data)

    return questionResponse_list


def createQuestionDetails(data):
    questions = []
   
    if "questions" in data and len(data["questions"]): 

        for index, question in enumerate(data["questions"]):
            questionDetail = QuestionDetail()
            questionDetail.set_data(question)
            questions.append(questionDetail)

    return questions

def createQuestionResponseSections(data):
    sections = []
    
    if "sections" in data and len(data["sections"]): 

        for index, aSection in enumerate(data["sections"]):
            questions = createQuestionDetails(aSection)
            questionResponseSection = QuestionResponseSection()
            questionResponseSection.set_data(aSection, questions)
            sections.append(questionResponseSection)

    return sections    
 
def getQuestionsData(questionResponseSection, data):
    data["questions"] = []
    
    if "questions" in questionResponseSection:
        for question in questionResponseSection.questions:
            aQuestion = {}
            aQuestion, questionId = question.get_data(aQuestion)
            aQuestion = question_service_module.questions.get_question_by_id(questionId, aQuestion); 
            data["questions"].append(aQuestion)

        return data  

def getSectionData(questionResponse, data):
    data["sections"] = []
    
    if "sections" in questionResponse:
        for section in questionResponse.sections:
            questionResponse_section = {}
            questionResponse_section = section.get_data(questionResponse_section)
            
            questionResponse_section = getQuestionsData(section, questionResponse_section)   
              
            data["sections"].append(questionResponse_section)

        return data          