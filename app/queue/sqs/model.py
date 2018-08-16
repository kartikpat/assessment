from mongoengine import *            

class Questionnaire(Document):
    associationMeta = DynamicField(db_field='associationMeta')
    associationPublished = DynamicField(db_field='associationPublished')
     

        





