from services import sendMessage, receiveMessage, deleteMessage
import json
from app.questionnaire.model.questionnaire import Questionnaire
from app.questionnaire.service.jobAssociation import associateJobWithQuestionnaire,updateMetaAndPublishAssociation, associatePublishWithMeta
from app.exception import InvalidObjectId
from mongoengine import connect

connect('development')  

try:
    while True:
        response = receiveMessage()
        if 'Messages' in response:
            for message in response['Messages']:
                responseBody = json.loads(message['Body'])
                receipt_handle = message['ReceiptHandle']

                if(responseBody["event"] == "post"):
                    data = {}
                    data["associationMeta"] = responseBody["metaId"]
                    for index, questionnaireId in enumerate(responseBody["questionnaire"]):
                        associateJobWithQuestionnaire(data, questionnaireId)

                elif(responseBody["event"] == "publish"):
                    associatePublishWithMeta(responseBody["publishId"], responseBody["metaId"])
                else:
                    updateMetaAndPublishAssociation(responseBody)
                            
                deleteMessage(receipt_handle)
        else:
            print('Queue is now empty')
            break   

except Questionnaire.DoesNotExist as e:
    message = 'questionnaire id doesn\'t exist'
    print(message)
        
except InvalidObjectId as e:
    message = 'questionnaire id is not valid'
    if hasattr(e, 'message'):
        e.to_dict()
        message = e.message
    print(message)

except Exception as e:
    print(e)    