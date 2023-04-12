from flask import Blueprint

blueprint = Blueprint("main", __name__)


@blueprint.route("/")
def index():
    return "Hello World!"
