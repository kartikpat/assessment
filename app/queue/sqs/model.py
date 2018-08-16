from mongoengine import *   

class QuestionnaireSection(EmbeddedDocument):
    id = IntField(db_field='id', min_value=0, required=True)
    type = StringField(db_field='type',required= True)
    questionIds = ListField(ObjectIdField(),db_field='questionIds', default=None)         

class Questionnaire(Document):
    associationMeta = DynamicField(db_field='associationMeta')
    associationPublished = DynamicField(db_field='associationPublished')
    sections = EmbeddedDocumentListField(QuestionnaireSection, db_field='sections')

class Question(Document): 
    availability = BooleanField(db_field='availability', default=False)    
     

        





