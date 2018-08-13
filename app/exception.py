class Error(Exception):
   """Base class for other exceptions.
    
    Attributes:
        message -- explanation of the error
        status_code -- custom http status code(optional)
        payload -- extra information(optional)
   """
   def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class BadContentType(Error):
    """Exception raised for invalid object id"""

    def __init__(self, message, status_code=None, payload=None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload


class FormValidationError(Error):
    """Exception raised for errors in the form validation"""
    def __init__(self, message, status_code=None, payload=None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

class InvalidObjectId(Error):
    """Exception raised for invalid object id"""
    def __init__(self, message, status_code=None, payload=None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

class EmbeddedDocumentNotFound(Error):
    """Exception Raised for Embedded Document in list of documents not found"""
    def __init__(self, message, status_code=None, payload=None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload                

class MissingGetParameters(Error):
    """Exception Raised for Missing get parameters"""
    def __init__(self, message, status_code=None, payload=None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload  

class EntityNotExists(Error):
    """Exception Raised for Embedded Document in list of documents not found"""
    def __init__(self, message, status_code=None, payload=None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload        

