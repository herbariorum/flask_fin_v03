# application/aluno/views.py

from flask import render_template, Blueprint

aluno = Blueprint('aluno', __name__, template_folder='templates')


@aluno.route("/")
def index():
    return render_template('aluno/index.html')