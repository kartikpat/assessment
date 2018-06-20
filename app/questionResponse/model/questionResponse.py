from mongoengine.document import Document
from mongoengine import *
from extras_mongoengine.fields import IntEnumField
import datetime
from app.questionResponse.enumerations import *
from app.questionResponse.constants import *
from app.utils import getDateInIsoFormat

class QuestionResponse(Document):
    _question = LazyReferenceField('Question', db_ref=False, db_field='questionId', required=True)
    _questionaire = LazyReferenceField('Questionaire',db_ref=False,db_field='questionaireId',required=True)
    _seekerId = LongField(db_field='seekerId', min_value=1, required = True)
    _assessedOn = DateTimeField(db_field='assessedOn', required=True)
    _timeTaken = IntField(db_field='timeTaken', min_value=0,default=0, required = True)
    
    def set_data(self, data):
        self._question = data["questionId"]
        self._questionaire = data["questionaireId"]
        self._seekerId = data["seekerId"]
        self._assessedOn = data["assessedOn"]
        if "timeTaken" in data:
            self._timeTaken = data["timeTaken"]                                   
        
    def get_data(self, data):
        data["id"] = str(self.id)
        data["question"] = str(self._question.pk)
        data["questionaireId"] = str(self._questionaire.pk)
        data["seekerId"] = self._seekerId
        data["assessedOn"] = getDateInIsoFormat(self._assessedOn)
        data["timeTaken"] = self._timeTaken  
        return data