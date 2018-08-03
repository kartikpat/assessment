from app.summary.model.summary import Summary
from bson import ObjectId
import bson
from ...exception import InvalidObjectId
from ...utils import is_valid_object_id

def insert_summary(data):

    summary = Summary()
    summary.set_data(data)

    summary.save()
    summary_id = str(summary.id)

    return summary_id

def update_summary(data, summary_id):
    if not is_valid_object_id(summary_id):
        raise InvalidObjectId('invalid summary id') 

    summary_o_id = ObjectId(summary_id)
    summary = Summary.objects.get(id=summary_o_id)

    summary.update_data(data)
    summary.save()

    return
    
def get_summary_list():
    summary_list = []
    for summary in Summary.objects:
        data = {}

        data = summary.get_data(data)

        summary_list.append(data)

    return summary_list

def get_summary(summary_id):
    if not is_valid_object_id(summary_id):
        raise InvalidObjectId('invalid summary id')    

    summary_o_id = ObjectId(summary_id)
    summary = Summary.objects.get(id=summary_o_id)
    data = {}
    
    data = summary.get_data(data)

    summary_list = []    
    summary_list.append(data)

    return summary_list
