from mongoengine.document import Document
from mongoengine import *
from extras_mongoengine.fields import IntEnumField
import datetime
from ..enumerations import *
from ..constants import *
from ...utils import getDateInIsoFormat, encode_objectId

class Question(Document): 
    question = StringField(db_field='question',required=True, unique=True)
    type = IntEnumField(QuestionType, db_field='type', required = True, default=QuestionType.MULTI)
    answerOptions = ListField(DynamicField(), db_field='answerOptions', default=None)
    answer = IntField(db_field='answer', min_value=0)
    createdAt = DateTimeField(db_field='createdAt',default=datetime.datetime.utcnow, required=True)
    updatedAt = DateTimeField(db_field='updatedAt')
    author = LongField(db_field='author', min_value=1, required = True)
    skillTags = ListField(LongField(min_value=0),db_field='skillTags', default=None)
    origin = IntEnumField(QuestionOrigin, db_field='origin')
    level = IntEnumField(QuestionLevel, db_field='level')
    availability = BooleanField(db_field='availability', default=False)
    mandatory = BooleanField(db_field='mandatory')
    
    def set_data(self, data):
        self.question = data["question"]
        if "type" in data:
            self.type = int(data["type"])
        if "answerOptions" in data:
            self.answerOptions = data["answerOptions"] 
        if "answer" in data:       
            self.answer = data["answer"]
        self.author = int(data["author"])
        if "skillTags" in data:
            self.skillTags = data["skillTags"]
        if "origin" in data:
            self.origin = data["origin"] 
        if "level" in data:
            self.level = data["level"]
        if "mandatory" in data:
            self.mandatory = data["mandatory"]        

    def update_data(self, data):
        if "question" in data:
            self.question = data["question"]
        if "type" in data:
            self.type = int(data["type"])   
        if "answerOptions" in data:   
            self.answerOptions = data["answerOptions"]
        if "answer" in data:   
            self.answer = data["answer"]        
        self._updatedAt = datetime.datetime.utcnow 
        if "skillTags" in data:   
            self.skillTags = data["skillTags"]
        if "level" in data:
            self.level = data["level"]                   
        if "origin" in data:
            self.level = data["level"]
        if "mandatory" in data:
            self.mandatory = data["mandatory"]    

    def get_data(self, data):
        data["id"] = encode_objectId(self.id)
        data["question"] = self.question
        data["type"] = int(self.type.value)
        if "answerOptions" in self and self.answerOptions:
            data["answerOptions"] = self.answerOptions
        if "answer" in self:    
            data["answer"] = self.answer
        data["createdAt"] = getDateInIsoFormat(self.createdAt)
        if "updatedAt" in self:
            data["updatedAt"] = getDateInIsoFormat(self.updatedAt)
        data["author"] = self.author  
        if "skillTags" in self:
            data["skillTags"] = self.skillTags  
        if "origin" in self:    
            data["origin"] = int(self.origin.value)
        if "level" in self:    
            data["level"] = int(self.level.value)
        if "mandatory" in self:
            data["mandatory"] = self.mandatory   
        return data 

        





