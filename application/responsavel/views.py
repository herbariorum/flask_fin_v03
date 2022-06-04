# application/responsavel/views.py

from flask import render_template, Blueprint

responsavel = Blueprint('responsavel', __name__, template_folder='templates')


@responsavel.route("/")
def index():
    return render_template('index.html')

