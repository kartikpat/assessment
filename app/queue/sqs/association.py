from services import sendMessage, receiveMessage, deleteMessage
   
try:
	sendMessage('association keys',{
	    'metaOld': { 
	    	'DataType': 'Number',
            'StringValue': "333033" 
        },
	    'publishedOld': { 
	    	'DataType': 'Number',
            'StringValue': "334895"
        },
	    'metaNew': { 
	    	'DataType': 'Number',
            'StringValue': "123456"
        },
	    'publishedNew': { 
	    	'DataType': 'Number',
            'StringValue': "334896"
        }
	})

except Exception as e:
    print(e)	

# try:
# 	response = receiveMessage()

# 	message = response['Messages'][0]
# 	receipt_handle = message['ReceiptHandle']

# 	print(message)

# 	deleteMessage(receipt_handle)

	

# except Exception as e:
# 	print(e)	