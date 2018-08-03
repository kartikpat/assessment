from app.questionResponse.model.questionResponse import QuestionResponse, QuestionDetail, QuestionResponseSection
from bson import ObjectId
import bson
from ...exception import InvalidObjectId
from ...utils import is_valid_object_id, decode_objectId, encode_objectId
from mongoengine.queryset.visitor import Q
from ...questions.service.questions import getQuestionReference

def get_seekers(questionaire_id, questions):
    questionaire_id = decode_objectId(questionaire_id)
    if not is_valid_object_id(questionaire_id):
        raise InvalidObjectId('invalid questionaire id')

    data = []

    if not questions:
        questionResponse = QuestionResponse.objects(questionaireId= questionaire_id).only('seeker');
        for aQuestionResponse in questionResponse:
            data.append(aQuestionResponse.seeker) 

        return data    
    
    for index, aQuestion in enumerate(questions):
        question = getQuestionReference(aQuestion["id"])
        type = int(question.type.value);
        temp = []
        if index > 0 and not data:
            return data
        
        if(type == 1):   
            pipeline = [
                        {"$match": {"questionaireId": questionaire_id }},
                        {"$project":{
                            "sections":{
                                "$filter":{
                                    "input":{
                                        "$map":{
                                            "input": "$sections",
                                            "as": "section",
                                            "in": {
                                                "questions":{
                                                    "$filter":{
                                                        "input": "$$section.questions",
                                                        "as": "question",
                                                        "cond":{
                                                            "$and": [{"$eq":["$$question.id",decode_objectId(aQuestion["id"])]},
                                                                     {"$setIsSubset":  [ "$$question.answer",aQuestion["answer"]]}]
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    "as": "section",
                                    "cond": { "$ne": [ "$$section.questions", [] ]}
                                }
                            }, "_id":0, "seeker":1
                        }}
                       ]

    
            questionResponse = QuestionResponse.objects.aggregate(*pipeline)
            
            for aQuestionResponse in questionResponse:
                if aQuestionResponse["sections"]:
                    temp.append(aQuestionResponse["seeker"]) 

        elif(type == 2 or type == 3):   
            pipeline = [
                        {"$match": {"questionaireId": ObjectId("5b5db49a15f9e55f97b34567") }},
                        {"$project":{
                            "sections":{
                                "$filter":{
                                    "input":{
                                        "$map":{
                                            "input": "$sections",
                                            "as": "section",
                                            "in": {
                                                "questions":{
                                                    "$filter":{
                                                        "input": "$$section.questions",
                                                        "as": "question",
                                                        "cond":{
                                                            "$and": [{"$eq":["$$question.id", decode_objectId(aQuestion["id"])]},
                                                                     {"$in":  [ "$$question.answer", aQuestion["answer"]]}]
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    "as": "section",
                                    "cond": { "$ne": [ "$$section.questions", [] ]}
                                }
                            }, "_id":0, "seeker":1
                        }}
                       ]

    
            questionResponse = QuestionResponse.objects.aggregate(*pipeline)
            for aQuestionResponse in questionResponse:
                if aQuestionResponse["sections"]:
                    temp.append(aQuestionResponse["seeker"])     

        elif(type == 4 or type == 5):   
            pipeline = [
                        {"$match": {"questionaireId": ObjectId("5b5db49a15f9e55f97b34567") }},
                        {"$project":{
                            "sections":{
                                "$filter":{
                                    "input":{
                                        "$map":{
                                            "input": "$sections",
                                            "as": "section",
                                            "in": {
                                                "questions":{
                                                    "$filter":{
                                                        "input": "$$section.questions",
                                                        "as": "question",
                                                        "cond":{
                                                            "$eq":["$$question.id", decode_objectId(aQuestion["id"])]
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    "as": "section",
                                    "cond": { "$ne": [ "$$section.questions", [] ]}
                                }
                            }, "_id":0, "seeker":1
                        }}
                       ]

    
            questionResponse = QuestionResponse.objects.aggregate(*pipeline)
            for aQuestionResponse in questionResponse:
                if aQuestionResponse["sections"] and aQuestion["answer"] == 1:
                    temp.append(aQuestionResponse["seeker"])
                elif not aQuestionResponse["sections"] and aQuestion["answer"] == 0:      
                    temp.append(aQuestionResponse["seeker"])

        if index == 0:
            data = temp;

        data = list(set(temp) & set(data)); 

    return data    



