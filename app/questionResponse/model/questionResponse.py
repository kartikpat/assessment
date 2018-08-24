from mongoengine.document import Document
from mongoengine import *
from extras_mongoengine.fields import IntEnumField
import datetime
from ..enumerations import *
from ...enumerations import Invocation
from ..constants import *
from ...utils import getDateInIsoFormat, encode_objectId, decode_objectId
 
class QuestionDetail(EmbeddedDocument):
    id = ObjectIdField(db_field='id', required=True)
    answer = DynamicField(db_field='answer')

    def set_data(self, data): 
        self.id = decode_objectId(data["id"])
        if "answer" in data:
            self.answer = data["answer"]                                       
        
    def get_data(self, data):
        questionId = encode_objectId(self.id)
        data["answer"] = self.answer 
        return data, questionId

class QuestionResponseSection(EmbeddedDocument):
    id = IntField(db_field='id', min_value=0, required=True)  
    questions = EmbeddedDocumentListField(QuestionDetail, db_field='questions')   

    def set_data(self, data, questions): 
        self.id = int(data["id"])
        if questions:
            self.questions = questions                                       
        
    def get_data(self, data):
        data["id"] = self.id; 
        return data

class QuestionResponse(Document):
    sections = EmbeddedDocumentListField(QuestionResponseSection, db_field='sections')
    questionnaireId = ObjectIdField(db_field='questionnaireId',required=True)
    seeker = LongField(db_field='seeker', min_value=1, required = True)
    associationPublished = LongField(db_field='associationPublished', required=True)
    assessedOn = DateTimeField(db_field='assessedOn',default=datetime.datetime.utcnow, required=True)
    invocation = IntEnumField(Invocation, db_field='invocation', required=True)
    timeTaken = IntField(db_field='timeTaken')

    meta = {
        'indexes': [
            {
                'fields': ['associationPublished', 'invocation', 'seeker'],
                'unique': True 
            },
            {
                'fields': ['associationPublished', 'invocation'] 
            }
        ]
    }
    
    def set_data(self, data, sections):
        self.questionnaireId = decode_objectId(data["questionnaireId"])
        self.seeker = int(data["seeker"])
        if "assessedOn" in data:
            self.assessedOn = data["assessedOn"]
        self.associationPublished = int(data["associationPublished"])
        self.invocation = int(data["invocation"])
        if "timeTaken" in data:
            self.timeTaken = data["timeTaken"]
        if sections:
            self.sections = sections                                       
        
    def get_data(self, data):
        data["id"] = encode_objectId(self.id)
        data["questionnaireId"] = encode_objectId(self.questionnaireId)
        data["seeker"] = self.seeker
        data["assessedOn"] = getDateInIsoFormat(self.assessedOn)
        data["associationPublished"] = self.associationPublished
        data["invocation"] = int(self.invocation.value)
        if "timeTaken" in self:
            data["timeTaken"] = self.timeTaken  
        return data