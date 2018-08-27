from flask import make_response,jsonify
import jwt
secretKey = "iimjobs__screeningtoken!!"
from ..exception import NotAuthorized   
def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: boolean|string
    """
    try:
        payload = jwt.decode(auth_token, secretKey, algorithms=['HS256'])
        return True, payload

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        raise NotAuthorized('You are not authorized to use this service')
