from flask import abort
import jwt
secretKey = "\xa4\xc9\xd4\x954,\xc4\xaa\xa0H\x01\xe4vY\xe8\xda\xa6\x81\x11\x8eg\xb3oM"

def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: boolean|string
    """
    try:
        payload = jwt.decode(auth_token, secretKey)
        return True

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        logger.exception(e)
        message = 'Not Authorized'
        abort(403,{'message': message})