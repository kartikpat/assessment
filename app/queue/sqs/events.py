from sqs_services import sendMessage, receiveMessage, deleteMessage
import json
from model import Questionnaire
from services import associateJobWithQuestionnaire,updateMetaAndPublishAssociation, associatePublishWithMeta
from mongoengine import connect
import time

connect('development')  

try:
    startSec = int(round(time.time()))
    while True:
        response = receiveMessage();
        if 'Messages' in response:
            for message in response['Messages']:
                responseBody = json.loads(message['Body'])
                receipt_handle = message['ReceiptHandle']
                print(responseBody)
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
            print('Queue is now empty');
            newSec = int(round(time.time()))
            if((newSec - startSec) > 50):
                print("breaking")
                break
            else:   
                print("continue") 
                continue
      
            

except Questionnaire.DoesNotExist as e:
    message = 'questionnaire id doesn\'t exist'
    print(message)

except Exception as e:
    print(e)       