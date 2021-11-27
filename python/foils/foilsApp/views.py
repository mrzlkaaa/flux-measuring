from flask import Blueprint


view = Blueprint('view', __name__)

@view.route("/")
def hello():
    return "hello"