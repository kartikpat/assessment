from mongoengine import *
from extras_mongoengine.fields import IntEnumField
import datetime
from ..enumerations import AuthorType, QuestionaireStatus
from ...enumerations import Invocation 
from ..constants import questionaireViewType, questionaireSectionType
from ...utils import getBooleanValue, getDateInIsoFormat, encode_objectId , decode_objectId

class QuestionaireProperty(EmbeddedDocument):
    viewType = StringField(db_field='viewType', choices=questionaireViewType)
    showAnswers = BooleanField(db_field='showAnswers')
    durationInMin = IntField(db_field='durationInMin', min_value = 0)
    blockWindow = BooleanField(db_field='blockWindow')

    def set_data(self, data):
        if "viewType" in data:
            self.viewType = data["viewType"]
        if "showAnswers" in data:
            self.showAnswers = data["showAnswers"]
        if "durationInMin" in data:
            self.durationInMin = data["durationInMin"]
        if "blockWindow" in data:
            self.blockWindow = getBooleanValue(data["blockWindow"])    

    def update_data(self, data):  
        if "viewType" in data:
            self.viewType = data["viewType"]
        if "showAnswers" in data:
            self.showAnswers = data["showAnswers"]
        if "durationInMin" in data:
            self.durationInMin = data["durationInMin"]  
        if "blockWindow" in data:
            self.blockWindow = getBooleanValue(data["blockWindow"])

    def get_data(self, data):
        if "viewType" in self:
            data["viewType"] = self.viewType
        if "showAnswers" in self:
            data["showAnswers"] = self.showAnswers
        if "durationInMin" in self:
            data["durationInMin"] = self.durationInMin
        if "blockWindow" in self:
            data["blockWindow"] = self.blockWindow 
        return data    

class QuestionaireSection(EmbeddedDocument):
    id = IntField(db_field='id', min_value=0, required=True)
    heading = StringField(db_field='heading')
    type = StringField(db_field='type',required= True, choices=questionaireSectionType)
    noOfQuestion = IntField(min_value=0, db_field='noOfQuestion')
    skillTags = ListField(LongField(min_value=0),db_field='skillTags', default=None)
    questionIds = ListField(ObjectIdField(),db_field='questionIds', default=None)

    def set_data(self, data, s_id):
        self.id = s_id
        if "heading" in data:
            self.heading = data["heading"]
        self.type = data["type"]
        if data["type"] == "static":
            data["questionIds"] = list(map(decode_objectId, data["questionIds"]))
            self.questionIds = data["questionIds"]
        elif data["type"] == "dynamic":
            self.noOfQuestion = data["noOfQuestion"]
            self.skillTags = data["skillTags"]
         
    def update_data(self, data):
        if "heading" in data:
            self.heading = data["heading"]
 
        if data["type"] == "static":
            data["questionIds"] = list(map(decode_objectId, data["questionIds"]))
            self.questionIds = data["questionIds"]
        
        elif data["type"] == "dynamic":
            self.noOfQuestion = data["noOfQuestion"]
            self.skillTags = data["skillTags"]            

    def get_data(self, data):
        data["id"] = self.id
        if "heading" in self:
            data["heading"] = self.heading
        data["type"] = self.type

        if data["type"] == "static":
            questionIds = self.questionIds
              
        elif data["type"] == "dynamic":
            data["noOfQuestion"] = self.noOfQuestion
            data["skillTags"] = self.skillTags

        return data, questionIds               

class Questionaire(Document):
    name = DynamicField(db_field='name')
    author = DynamicField(db_field='author',required=True)
    authorType = IntEnumField(AuthorType, db_field='authorType', required = True)
    associationMeta = DynamicField(db_field='associationMeta')
    associationPublished = DynamicField(db_field='associationPublished')
    createdAt = DateTimeField(db_field='createdAt',default=datetime.datetime.utcnow, required=True)
    updatedAt = DateTimeField(db_field='updatedAt')
    status = IntEnumField(QuestionaireStatus, default=QuestionaireStatus.SAVED, db_field='status',required=True)
    tags = DictField(db_field='tags', default=None)
    invocation = IntEnumField(Invocation, db_field='invocation', required=True)
    description = StringField(db_field='description')
    instruction = StringField(db_field='instruction')
    property = EmbeddedDocumentField(QuestionaireProperty, db_field='property', default=None)
    sections = EmbeddedDocumentListField(QuestionaireSection, db_field='sections')

    meta = {
        'indexes': [
            {
                'fields': ['associationMeta', 'invocation'],
                'unique': True 
            },
            {
                'fields': ['associationPublished', 'invocation'],
                'unique': True 
            }
        ]
    }
    
    def set_data(self, data, q_property, q_sections):
        if "name" in data:
            self.name = data["name"]
        self.authorType = data["authorType"]
        self.author = data["author"]  
        self.associationMeta = data["associationMeta"]      
        self.invocation = data["invocation"]  
        if "associationPublished" in data:
            self.associationPublished = data["associationPublished"]
        if "description" in data:
            self.description = data["description"]        
        if "instruction" in data:
            self.instruction = data["instruction"]
        if "tags" in data:
            self.tags = data["tags"]
        if q_property:
            self.property = q_property            
        self.sections = q_sections 

    def update_data(self, data, q_property, q_sections):
        if "name" in data:
            self.name = data["name"]
        if "description" in data:
            self.description = data["description"]
        self.updatedAt = datetime.datetime.utcnow 
        if "status" in data:   
            self.status = data["status"]
        if "instruction" in data:   
            self.instruction = data["instruction"]
        if q_property:    
            self.property = q_property
        self.sections = q_sections                   
        
    def get_data(self, data):
        data["id"] = encode_objectId(self.id)
        if "name" in self and self.name: 
            data["name"] = self.name
        if "description" in self and self.description:
            data["description"] = self.description
        if "tags" in self and self.tags:    
            data["tags"] = self.tags
        data["authorType"] = int(self.authorType.value)
        data["createdAt"] = getDateInIsoFormat(self.createdAt)
        if "updated" in self and self.updated:
            data["updatedAt"] = getDateInIsoFormat(self.updatedAt)
        data["status"] = int(self.status.value)
        data["invocation"] = int(self.invocation.value)
        if "instruction" in self and self.instruction:
            data["instruction"] = self.instruction

        return data 

        





