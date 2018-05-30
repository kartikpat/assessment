from app.model.assessment.model import Assessment
from bson import ObjectId
import bson
from app.error.exception import InvalidObjectId


def create_assessment(data):
    assessment = Assessment()
    assessment.set_value(data)
    assessment.save()
    assessment_id = str(assessment.id)
    return assessment_id

def update_assessment(data, assessment_id):
    if(not bson.objectid.ObjectId.is_valid(assessment_id)):
        raise InvalidObjectId('invalid assessment id')
    assessment_o_id = ObjectId(assessment_id)
    assessment = Assessment.objects.get(id=assessment_o_id)
    assessment.set_value(data)
    assessment.save()
    return
    
def fetch_assessment_list():
    assessment_list = []
    for assessment in Assessment.objects:
        data = {}
        data = assessment.get_value(data)
        assessment_list.append(data)

    return assessment_list

def fetch_assessment(assessment_id):
    data = {}
    if(not bson.objectid.ObjectId.is_valid(assessment_id)):
        raise InvalidObjectId('invalid assessment id') 
    assessment_o_id = ObjectId(assessment_id)
    assessment = Assessment.objects.get(id=assessment_o_id)
    assessment.get_value(data)
    assessment_list = []
    assessment_list.append(data)

    return assessment_list