from app.questionaire.model.questionaire import Questionaire, QuestionaireProperty, QuestionaireSecurity, QuestionaireSection
from bson import ObjectId
import bson
from app.exception import InvalidObjectId, EmbeddedDocumentNotFound
from app.utils import is_valid_object_id


def insert_questionaire(data):

    if "sections" in data and len(data["sections"]):
        sections = [] 
        for index, section in enumerate(data["sections"]):
            questionaire_section = QuestionaireSection()
            section_id = index;
            questionaire_section.set_data(section, section_id)
            sections.append(questionaire_section)

    questionaire_security = QuestionaireSecurity()
    questionaire_security.set_data(data)

    questionaire_property = QuestionaireProperty()
    questionaire_property.set_data(data, questionaire_security)

    questionaire = Questionaire()
    questionaire.set_data(data, questionaire_property, sections)

    questionaire.save()
    questionaire_id = str(questionaire.id)

    return questionaire_id

def update_questionaire(data, questionaire_id):
    if not is_valid_object_id(questionaire_id):
        raise InvalidObjectId('invalid questionaire id') 

    questionaire_o_id = ObjectId(questionaire_id)
    questionaire = QuestionResponse.objects(id=questionaire_o_id).no_dereference().first()
    if not questionaire:
        raise Questionaire.DoesNotExist

    questionaire._property._security.update_data(data)
    questionaire._property.update_data(data)

    if "sections" in data and len(data["sections"]):
        for index, section in enumerate(data["sections"]):
            for db_section in questionaire._sections:
                if db_section._id == section["id"]:
                    q_section = db_section
                    break
                else:
                    message = 'id for section-'+str(index)+' doesn\'t exist'
                    raise EmbeddedDocumentNotFound(message)
            q_section.update_data(section)

    questionaire.update_data(data)
    questionaire.save()

    return
    
def get_questionaire_list():
    questionaire_list = []

    for questionaire in Questionaire.objects:
        data = {}
        data = questionaire._property._security.get_data(data)
        data = questionaire._property.get_data(data)

        data = getSectionData(questionaire, data)

        data = questionaire.get_data(data)

        questionaire_list.append(data)

    return questionaire_list

def get_questionaire(questionaire_id):
    if not is_valid_object_id(questionaire_id):
        raise InvalidObjectId('invalid questionaire id')    

    questionaire_o_id = ObjectId(questionaire_id)
    questionaire = QuestionResponse.objects(id=questionaire_o_id).no_dereference().first()
    if not questionaire:
        raise Questionaire.DoesNotExist

    data = {}

    data = questionaire._property._security.get_data(data)
    data = questionaire._property.get_data(data)
    
    data = getSectionData(questionaire, data)

    data = questionaire.get_data(data)

    questionaire_list = []    
    questionaire_list.append(data)

    return questionaire_list


def getSectionData(questionaire, data):
    data["sections"] = []
    for section in questionaire._sections:
        q_section = {}
        q_section = section.get_data(q_section)
        data["sections"].append(q_section)
    return data
