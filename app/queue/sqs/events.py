from services import sendMessage, receiveMessage, deleteMessage
import json
from app.questionaire.model.questionaire import Questionnaire
from app.questionaire.service.jobAssociation import associateJobWithQuestionnaire,updateMetaAndPublishAssociation, associatePublishWithMeta
from app.exception import InvalidObjectId
from mongoengine import connect

connect('development')	

try:
	response = receiveMessage()

	message = response['Messages'][0]
	receipt_handle = message['ReceiptHandle']

	responseBody = json.loads(message['Body'])
	
	if(responseBody["event"] == "post"):
		data = {}
		data["associationMeta"] = responseBody["metaId"]
		for index, questionaireId in enumerate(responseBody["questionaire"]):
			associateJobWithQuestionnaire(data, questionaireId)

	elif(responseBody["event"] == "publish"):
		associatePublishWithMeta(responseBody["publishId"], responseBody["metaId"])
	else:
		updateMetaAndPublishAssociation(responseBody)		
	
	deleteMessage(receipt_handle)

except Questionnaire.DoesNotExist as e:
    message = 'questionaire id doesn\'t exist'
    print(message)
        
except InvalidObjectId as e:
    message = 'questionaire id is not valid'
    if hasattr(e, 'message'):
        e.to_dict()
        message = e.message
    print(message)

except Exception as e:
	print(e)	