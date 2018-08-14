from mongoengine.document import Document
from mongoengine import *
from extras_mongoengine.fields import IntEnumField
import datetime
from ..enumerations import *
from ..constants import *
from ...utils import getDateInIsoFormat

class Summary(Document):
    _questionnaire = LazyReferenceField('Questionnaire',db_ref=False,db_field='questionnaireId',required=True, reverse_delete_rule=CASCADE)
    _seekerId = LongField(db_field='seekerId', min_value=1, required = True)
    _assessedOn = DateTimeField(db_field='assessedOn', required=True)
    _timeTaken = IntField(db_field='timeTaken', min_value=0,default=0, required = True)
    _noOfCorrects = IntField(db_field='corrects',min_value=0)
    _noOfWrongs = IntField(db_field='wrongs', min_value=0)
    _score = IntField(db_field='score')
    
    def set_data(self, data):
        self._questionnaire = data["questionnaireId"]
        self._seekerId = data["seekerId"]
        self._assessedOn = data["assessedOn"]
        if "timeTaken" in data:
            self._timeTaken = data["timeTaken"]
        if "corrects" in data:
            self._corrects = data["corrects"]
        if "wrongs" in data:
            self._wrongs = data["wrongs"]
        if "score" in data:
            self._score = data["score"]                                   
        
    def get_data(self, data):
        data["id"] = str(self.id)
        data["questionnaireId"] = str(self._questionnaire.pk)
        data["seekerId"] = self._seekerId
        data["assessedOn"] = getDateInIsoFormat(self._assessedOn)
        data["timeTaken"] = self._timeTaken
        if self._noOfCorrects:
            data["corrects"] = self._noOfCorrects
        if self._noOfWrongs:
            data["wrongs"] = self._noOfWrongs      
        if self._score:
            data["score"] = self._score  
        return data 

        





