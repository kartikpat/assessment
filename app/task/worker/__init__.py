from flask import Blueprint

celery_worker = Blueprint('celery_worker', __name__)

from . import worker