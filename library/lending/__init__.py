from flask import Blueprint

lending = Blueprint('lending', __name__)
from library.lending import views