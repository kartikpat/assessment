from app.questionResponse.model.questionResponse import QuestionResponse, QuestionDetail, QuestionResponseSection
from bson import ObjectId
import bson
from ...exception import InvalidObjectId
from ...utils import is_valid_object_id, decode_objectId, encode_objectId
from mongoengine.queryset.visitor import Q
from ...questions.service.questions import getQuestionReference

def get_seekers(associationPublished, questions, invocation):
    data = []
    if not questions:
        questionResponse = QuestionResponse.objects(Q(associationPublished=int(associationPublished)) & Q(invocation=int(invocation))).only('seeker');

        for aQuestionResponse in questionResponse:
            data.append(aQuestionResponse.seeker) 

        return data    
    
    for index, aQuestion in enumerate(questions):
        question = getQuestionReference(aQuestion["id"])
        type = int(question.type.value);
        matchingSeekers = []
        if index > 0 and not data:
            return data
        if(type == 1):  
            for innerIndex, anAnswer in enumerate(aQuestion["answer"]):
                temp = []
                pipeline = [
                            {"$match": {"associationPublished": int(associationPublished), "invocation": int(invocation) }},
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
                                                                "$and": [{"$eq": ["$$question.id",decode_objectId(aQuestion["id"])]},
                                                                         {"$in":  [ int(anAnswer), "$$question.answer"]}]
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

                if innerIndex == 0:
                    matchingSeekers = temp;        

                matchingSeekers = list(set(temp) | set(matchingSeekers))        

        elif(type == 2 or type == 3):   
            aQuestion["answer"] = list(map(int, aQuestion["answer"]))
            pipeline = [
                        {"$match": {"associationPublished": int(associationPublished), "invocation": int(invocation) }},
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
                    matchingSeekers.append(aQuestionResponse["seeker"])     

        elif(type == 4 or type == 5): 
            if(((0 in aQuestion["answer"]) or ("0" in aQuestion["answer"])) and ((1 in aQuestion["answer"]) or ("1" in aQuestion["answer"]))):
                questionResponse = QuestionResponse.objects(Q(associationPublished=int(associationPublished)) & Q(invocation=int(invocation))).only('seeker');
                for aQuestionResponse in questionResponse:
                    matchingSeekers.append(aQuestionResponse.seeker) 

            else:    
                pipeline = [
                            {"$match": {"associationPublished": int(associationPublished), "invocation": int(invocation) }},
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
                    if aQuestionResponse["sections"] and ((1 in aQuestion["answer"]) or ("1" in aQuestion["answer"])):
                        matchingSeekers.append(aQuestionResponse["seeker"])
                    elif not aQuestionResponse["sections"] and ((0 in aQuestion["answer"]) or ("0" in aQuestion["answer"])):      
                        matchingSeekers.append(aQuestionResponse["seeker"])

        if index == 0:
            data = matchingSeekers;

        data = list(set(matchingSeekers) & set(data)); 

    return data    



