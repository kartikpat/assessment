from ..model.questionnaire import Questionaire, QuestionaireProperty, QuestionaireSection
from bson import ObjectId
import bson
from ...exception import InvalidObjectId, EmbeddedDocumentNotFound
from ...utils import is_valid_object_id, decode_objectId, encode_objectId
from mongoengine.queryset.visitor import Q
import app.questions.service as question_service_module
import app.questionResponse.service as questionResponse_service_module

def questionnaire_exist(data):
    if("associationMeta" in data):
        questionnaire = Questionaire.objects(Q(associationMeta=int(data["associationMeta"])) & Q(invocation=int(data["invocation"]))).only('id').first()
    if("associationPublished" in data):
        questionnaire = Questionaire.objects(Q(associationPublished=int(data["associationPublished"])) & Q(invocation=int(data["invocation"]))).only('id').first()    
    if questionnaire:
       return questionnaire.id

    return None     

def insert_questionnaire(data):

    questionnaire_sections = createQuestionaireSections(data)

    questionnaire_property = createQuestionaireProperty(data)

    questionnaire = Questionaire()
    questionnaire.set_data(data, questionnaire_property, questionnaire_sections)

    questionnaire.save()

    questionnaire_id = questionnaire.id
    return questionnaire_id

def update_questionnaire(data, questionnaire_id):
    questionnaire_id = decode_objectId(questionnaire_id)
    if not is_valid_object_id(questionnaire_id):
        raise InvalidObjectId('invalid questionnaire id') 

    questionnaire = Questionaire.objects(id=questionnaire_id).no_dereference().first()
    if not questionnaire:
        raise Questionaire.DoesNotExist

    questionnaire_property = createQuestionaireProperty(data)
 
    questionnaire_sections = createQuestionaireSections(data)
    
    questionnaire.update_data(data, questionnaire_property, questionnaire_sections)
    questionnaire.save()

    return
    
def get_questionnaire(parameters):
    questionnaire_list = []

    if parameters["associationMeta"] and parameters["invocation"]:
        questionnaire_objects = Questionaire.objects(Q(associationMeta=int(parameters["associationMeta"])) & Q(invocation=int(parameters["invocation"]))).no_dereference() 
    elif parameters["associationPublished"] and parameters["invocation"]:
        questionnaire_objects = Questionaire.objects(Q(associationPublished=int(parameters["associationPublished"])) & Q(invocation=int(parameters["invocation"]))).no_dereference() 
    elif parameters["associationMeta"]:
        questionnaire_objects = Questionaire.objects(Q(associationMeta=int(parameters["associationMeta"])))
    elif parameters["associationPublished"]:
        questionnaire_objects = Questionaire.objects(Q(associationPublished=int(parameters["associationPublished"])))
    else:
        questionnaire_objects = Questionaire.objects
    
    for questionnaire in questionnaire_objects:
        data = {}
    
        data = getQuestionaireData(questionnaire, data, parameters)

        questionnaire_list.append(data)

    return questionnaire_list

def get_questionnaire_by_id(questionnaire_id):
    questionnaire_id = decode_objectId(questionnaire_id) 
    if not is_valid_object_id(questionnaire_id):
        raise InvalidObjectId('invalid questionnaire id')    

    questionnaire = Questionaire.objects(id=questionnaire_id).no_dereference().first()
    if not questionnaire:
        raise Questionaire.DoesNotExist

    data = {}

    data = getQuestionaireData(questionnaire, data, None)

    questionnaire_list = []    
    questionnaire_list.append(data)

    return questionnaire_list

def getQuestionaireData(questionnaire, data, parameters):
    if "property" in questionnaire:
        data = questionnaire.property.get_data(data)
    
    data = getSectionData(questionnaire, data , parameters)

    data = questionnaire.get_data(data) 

    return data

def getSectionData(questionnaire, data, parameters):
    data["sections"] = []
    
    if "sections" in questionnaire:
        for section in questionnaire.sections:
            questionnaire_section = {}
            questionnaire_section, questionIds = section.get_data(questionnaire_section)
            
            if questionnaire_section["type"] == "static":
                questionnaire_section["questions"] = []
                for questionId in questionIds:
                    aQuestion = question_service_module.questions.get_question_by_id(encode_objectId(questionId), {});
                    
                    if parameters["seeker"]:
                        aQuestion = questionResponse_service_module.questionResponse.getQuestionResponse(aQuestion, parameters["seeker"], parameters["associationPublished"],parameters["invocation"] ,questionId, questionnaire_section["id"])
                    
                    questionnaire_section["questions"].append(aQuestion);
            
            elif questionnaire_section["type"] == "dynamic":
                data["noOfQuestion"] = self.noOfQuestion
                data["tags"] = self.tags

            data["sections"].append(questionnaire_section)

        return data

def createQuestionaireSections(data):
    questionnaire_sections = []
    
    if "sections" in data and len(data["sections"]): 

        for index, section in enumerate(data["sections"]):
            questionnaire_section = QuestionaireSection()
            section_id = index;
            questionnaire_section.set_data(section, section_id)
            questionnaire_sections.append(questionnaire_section)

    return questionnaire_sections    

def createQuestionaireProperty(data):
    questionnaire_property = QuestionaireProperty()
    questionnaire_property.set_data(data)

    return questionnaire_property