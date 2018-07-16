from ..model.questionaire import Questionaire, QuestionaireProperty, QuestionaireSection
from bson import ObjectId
import bson
from ...exception import InvalidObjectId, EmbeddedDocumentNotFound
from ...utils import is_valid_object_id, decode_objectId, encode_objectId
from mongoengine.queryset.visitor import Q
from ...questions.service.questions import get_question_by_id


def questionaire_exist(data):
    questionaire = Questionaire.objects(Q(association=data["association"]) & Q(invocation=data["invocation"])).only('id').first()
    if questionaire:
       return questionaire.id 

def insert_questionaire(data):

    questionaire_sections = createQuestionaireSections(data)

    questionaire_property = createQuestionaireProperty(data)

    questionaire = Questionaire()
    questionaire.set_data(data, questionaire_property, questionaire_sections)

    questionaire.save()

    questionaire_id = questionaire.id
    return questionaire_id

def update_questionaire(data, questionaire_id):
    questionaire_id = decode_objectId(questionaire_id)
    if not is_valid_object_id(questionaire_id):
        raise InvalidObjectId('invalid questionaire id') 

    questionaire = Questionaire.objects(id=questionaire_id).no_dereference().first()
    if not questionaire:
        raise Questionaire.DoesNotExist

    questionaire_property = createQuestionaireProperty(data)
 
    questionaire_sections = createQuestionaireSections(data)
    
    questionaire.update_data(data, questionaire_property, questionaire_sections)
    questionaire.save()

    return
    
def get_questionaire(parameters):
    questionaire_list = []

    if parameters["association"] and parameters["invocation"]:
        questionaire_objects = Questionaire.objects(Q(association=int(parameters["association"])) & Q(invocation=int(parameters["invocation"]))).no_dereference() 
    else:
        questionaire_objects = Questionaire.objects
    
    for questionaire in questionaire_objects:
        data = {}

        if "property" in questionaire:
            data = questionaire.property.get_data(data)

        data = getSectionData(questionaire, data)

        data = questionaire.get_data(data)

        questionaire_list.append(data)

    return questionaire_list

def get_questionaire_by_id(questionaire_id):
    questionaire_id = decode_objectId(questionaire_id) 
    if not is_valid_object_id(questionaire_id):
        raise InvalidObjectId('invalid questionaire id')    

    questionaire = Questionaire.objects(id=questionaire_id).no_dereference().first()
    if not questionaire:
        raise Questionaire.DoesNotExist

    data = {}

    if "property" in questionaire:
        data = questionaire.property.get_data(data)
    
    data = getSectionData(questionaire, data)

    data = questionaire.get_data(data)

    questionaire_list = []    
    questionaire_list.append(data)

    return questionaire_list

def getSectionData(questionaire, data):
    data["sections"] = []
    
    if "sections" in questionaire:
        for section in questionaire.sections:
            questionaire_section = {}
            questionaire_section, questionIds = section.get_data(questionaire_section)
            
            if questionaire_section["type"] == "static":
                questionaire_section["questions"] = []
                for questionId in questionIds:
                    questionaire_section["questions"].append(get_question_by_id(encode_objectId(questionId)));
            
            elif questionaire_section["type"] == "dynamic":
                data["noOfQuestion"] = self.noOfQuestion
                data["tags"] = self.tags

            data["sections"].append(questionaire_section)

        return data

def createQuestionaireSections(data):
    questionaire_sections = []
    
    if "sections" in data and len(data["sections"]): 

        for index, section in enumerate(data["sections"]):
            questionaire_section = QuestionaireSection()
            section_id = index;
            questionaire_section.set_data(section, section_id)
            questionaire_sections.append(questionaire_section)

    return questionaire_sections    

def createQuestionaireProperty(data):
    questionaire_property = QuestionaireProperty()
    questionaire_property.set_data(data)

    return questionaire_property