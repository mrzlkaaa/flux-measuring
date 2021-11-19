from flask import render_template, Blueprint

view = Blueprint('view', __name__)


@view.route("/")
def hello():
    return "Hello!"