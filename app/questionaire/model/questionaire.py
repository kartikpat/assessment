from mongoengine.document import Document
from mongoengine import *
from extras_mongoengine.fields import IntEnumField
import datetime
from app.questionaire.enumerations import AuthorType, QuestionaireStatus, QuestionaireInvocation
from app.questionaire.constants import questionaireViewType, questionaireSectionType
from app.utils import getBooleanValue, getDateInIsoFormat
from app.exception import ValidationError

class QuestionaireSecurity(EmbeddedDocument):
    _blockWindow = BooleanField(db_field='blockWindow', default=False)

    def set_data(self, data):
        if "blockWindow" in data:
            self._blockWindow = getBooleanValue(data["blockWindow"])

    def update_data(self, data):
        if "blockWindow" in data:
            self._blockWindow = getBooleanValue(data["blockWindow"])       

    def get_data(self, data):
        data["blockWindow"] = self._blockWindow 
        return data       

class QuestionaireProperty(EmbeddedDocument):
    _viewType = StringField(db_field='viewType', default='slide', choices=questionaireViewType)
    _showAnswers = BooleanField(db_field='showAnswers', default=False)
    _durationInMin = IntField(db_field='durationInMin', min_value = 0 , required=True, default=30)
    _security = EmbeddedDocumentField(QuestionaireSecurity, db_field='security') 

    def set_data(self, data, q_security):
        if "viewType" in data:
            self._viewType = data["viewType"]
        if "showAnswers" in data:
            self._showAnswers = data["showAnswers"]
        if "durationInMin" in data:
            self._durationInMin = data["durationInMin"]
        self._security = q_security

    def update_data(self, data):  
        if "viewType" in data:
            self._viewType = data["viewType"]
        if "showAnswers" in data:
            self._showAnswers = data["showAnswers"]
        if "durationInMin" in data:
            self._durationInMin = data["durationInMin"]  

    def get_data(self, data):
        data["viewType"] = self._viewType
        data["showAnswers"] = self._showAnswers
        data["durationInMin"] = self._durationInMin
        return data    

class QuestionaireSection(EmbeddedDocument):
    _id = IntField(db_field='id', min_value=0)
    _heading = StringField(db_field='heading')
    _type = StringField(db_field='type', default='static', choices=questionaireSectionType)
    _noOfQuestion = IntField(min_value=0, db_field='noOfQuestion')
    _tags = ListField(LongField(min_value=0, unique=True),db_field='tags', default=None)
    _questions = ListField(LongField(min_value=0, unique=True),db_field='questions', default=None)

    def set_data(self, data, s_id):
        self._id = s_id
        if "heading" in data:
            self._heading = data["heading"]
        self._type = data["type"]
        if data["type"] == "static":
            self._questions = data["questions"]
        
        elif data["type"] == "dynamic":
            self._noOfQuestion = data["noOfQuestion"]
            self._tags = data["tags"]
         

    def update_data(self, data):
        if "heading" in data:
            self._heading = data["heading"]

        if data["type"] == "static":
            self._questions = data["questions"]
        
        elif data["type"] == "dynamic":
            self._noOfQuestion = data["noOfQuestion"]
            self._tags = data["tags"]            

    def get_data(self, data):
        data["id"] = self._id
        data["heading"] = self._heading
        data["type"] = self._type

        if data["type"] == "static":
            data["questions"] = self._questions 
        
        elif data["type"] == "dynamic":
            data["noOfQuestion"] = self._noOfQuestion
            data["tags"] = self._tags

        return data               

class Questionaire(Document):
    _name = StringField(db_field='name',unique=True,required=True)
    _jobs = ListField(LongField(min_value=0, unique=True),db_field='jobs', default=None)
    _description = StringField(db_field='description')
    _author = LongField(db_field='author', min_value=1, required = True)
    _authorType = IntEnumField(AuthorType, db_field='authorType', required = True)
    _createdAt = DateTimeField(db_field='createdAt',default=datetime.datetime.utcnow, required=True)
    _updatedAt = DateTimeField(db_field='updatedAt')
    _status = IntEnumField(QuestionaireStatus, default=QuestionaireStatus.SAVED, db_field='status',required=True)
    _invocation = IntEnumField(QuestionaireInvocation, db_field='invocation', required=True, default=QuestionaireInvocation.APPLY)
    _instruction = StringField(db_field='instruction')
    _property = EmbeddedDocumentField(QuestionaireProperty, db_field='property')
    _sections = ListField(EmbeddedDocumentField(QuestionaireSection), db_field='sections')

    
    def set_data(self, data, q_property, q_sections):
        self._name = data["name"]
        if "jobs" in data:
            self._jobs = data["jobs"]
        if "description" in data:
            self._description = data["description"]
        self._author = data["author"]
        self._authorType = data["authorType"]
        self._invocation = data["invocation"]
        if "instruction" in data:
            self._instruction = data["instruction"]
        self._property = q_property
        self._sections = q_sections 

    def update_data(self, data):
        if "description" in data:
            self._description = data["description"]
        self._updatedAt = datetime.datetime.utcnow 
        if "status" in data:   
            self._status = data["status"]
        if "invocation" in data:   
            self._invocation = data["invocation"]
        if "instruction" in data:   
            self._instruction = data["instruction"]
        if "jobs" in data:
            self._jobs = data["jobs"]                   
        
    def get_data(self, data):
        data["id"] = str(self.id)
        data["name"] = self._name
        if self._description:
            data["description"] = self._description
        data["author"] = self._author
        data["authorType"] = int(self._authorType.value)
        data["createdAt"] = getDateInIsoFormat(self._createdAt)
        if self._jobs:
            data["jobs"] = self._jobs
        if self._updatedAt:
            data["updatedAt"] = getDateInIsoFormat(self._updatedAt)
        data["status"] = int(self._status.value)
        data["invocation"] = int(self._invocation.value)
        if self._instruction:
            data["instruction"] = self._instruction
        return data 

        





