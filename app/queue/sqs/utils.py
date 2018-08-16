from bson import ObjectId
from itsdangerous import base64_encode

def decode_objectId(value):
    return ObjectId(base64_decode(value))