from flask import Blueprint

questionResponse = Blueprint('questionResponse', __name__)

from . import route