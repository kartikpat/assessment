from sqs_services import sendMessage, receiveMessage, deleteMessage
import json
from model import Questionnaire
from services import associateJobWithQuestionnaire,updateMetaAndPublishAssociation, associatePublishWithMeta
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

except Exception as e:
    print(e)       