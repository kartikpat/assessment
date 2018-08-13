from flask import Blueprint

getSeekers = Blueprint('getSeekers', __name__)

from . import route