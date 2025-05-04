from flask import Blueprint

books = Blueprint('books', __name__)

from library.Books import views