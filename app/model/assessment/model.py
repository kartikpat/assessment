from mongoengine.document import Document
from mongoengine import *
import datetime

class Assessment(Document):
    _name = StringField(db_field='name',max_length=50)
    _status = IntField(db_field='status',required=True, default=0, min_value=0)
    _type = IntField(db_field='type',required=True, default=0, min_value=0)
    _assessor = IntField(db_field='assessor',required=True, default=0, min_value=0)
    _created_at = DateTimeField(db_field='created_at',default=datetime.datetime.utcnow, required=True)
    _last_updated = DateTimeField(db_field='last_updated')
    _duration_min = IntField(db_field='duration_min', required=True, default=30, min_value=1)
    _security = IntField(db_field='security',default=0, min_value=0)
    _invocation = IntField(db_field='invocation',default=0, min_value=0)
    _expiry = DateTimeField(db_field='expiry')
    _quesbank_type = IntField(db_field='quesbank_type',default=0, min_value=0)
    _description = StringField(db_field='description')
    _instruction = StringField(db_field='instruction')
    
    def set_value(self, data):
        self._name = data["name"] or ""
        self._status = data["status"] or 0
        self._type = data["type"] or 0
        self._assessor = data["assessor"] or 0
        self._created_at = data["created"] or datetime.datetime.utcnow
        self._last_updated = data["lastUpdated"] or None
        self._duration_min = data["durationInMin"] or 30
        self._security = data["security"] or 0
        self._invocation = data["invocation"] or 0
        self._expiry = data["expiry"] or None
        self._quesbank_type = data["quesbankType"] or 0
        self._description = data["description"] or ""
        self._instruction = data["instruction"] or "" 

    def get_value(self, data):
        data["id"] = str(self.id)
        data["name"] = self._name
        data["status"] = self._status
        data["type"] = self._type
        data["assessor"] = self._assessor
        data["created"] = self._created_at
        data["lastUpdated"] = self._last_updated
        data["durationInMin"] = self._duration_min
        data["security"] = self._security
        data["invocation"] = self._invocation
        data["expiry"] = self._expiry
        data["quesbankType"] = self._quesbank_type
        data["description"] = self._description
        data["instruction"] = self._instruction
        return data   