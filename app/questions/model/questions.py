from mongoengine.document import Document
from mongoengine import *
from extras_mongoengine.fields import IntEnumField
import datetime
from app.questions.enumerations import *
from app.questions.constants import *
from app.utils import getDateInIsoFormat

class Question(Document):
    _question = StringField(db_field='question',required=True)
    _type = IntEnumField(QuestionType, db_field='type', required = True, default=QuestionType.MCQ)
    _answerOptions = ListField(DynamicField(), db_field='ansOptions', required = True)
    _answer = IntField(db_field='answer', min_value=0, required = True)
    _createdAt = DateTimeField(db_field='createdAt',default=datetime.datetime.utcnow, required=True)
    _updatedAt = DateTimeField(db_field='updatedAt')
    _createdBy = LongField(db_field='createdBy', min_value=1, required = True)
    _tags = ListField(LongField(min_value=0, unique=True),db_field='tags', default=None)
    _origin = IntEnumField(QuestionOrigin, db_field='origin', default=QuestionOrigin.OTHERS)
    _level = IntEnumField(QuestionLevel, db_field='level')
    
    def set_data(self, data):
        self._question = data["question"]
        if "type" in data:
            self._type = data["type"]
        self._answerOptions = data["ansOptions"]
        self._answer = data["answer"]
        self._createdBy = data["createdBy"]
        if "tags" in data:
            self._tags = data["tags"]
        if "origin" in data:
            self._origin = data["origin"] 
        if "level" in data:
            self._level = data["level"]    

    def update_data(self, data):
        if "question" in data:
            self._question = data["question"]
        if "ansOptions" in data:   
            self._answerOptions = data["ansOptions"]
        if "answer" in data:   
            self._answer = data["answer"]        
        self._updatedAt = datetime.datetime.utcnow 
        if "tags" in data:   
            self._tags = data["tags"]
        if "level" in data:
            self._level = data["level"]                   
        
    def get_data(self, data):
        data["id"] = str(self.id)
        data["question"] = self._question
        data["type"] = int(self._type.value)
        data["ansOptions"] = self._answerOptions
        data["answer"] = self._answer
        data["createdAt"] = getDateInIsoFormat(self._createdAt)
        if self._updatedAt:
            data["updatedAt"] = getDateInIsoFormat(self._updatedAt)
        data["createdBy"] = self._createdBy  
        if self._tags:
            data["tags"] = self._tags  
        data["origin"] = int(self._origin.value)
        data["level"] = int(self._level.value)
        return data 

        





