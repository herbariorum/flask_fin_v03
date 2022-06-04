# application/admin/views.py
from flask import render_template, Blueprint
from ..auth.views import login_required


admin = Blueprint('admin', __name__)


@admin.route("/painel")
@login_required
def painel():
    return render_template('admin/painel.html', title = 'Finance')


@admin.route("/profile")
@login_required
def profile():
    return 'Profile'

@admin.route("/aluno")
@login_required
def aluno():
    return 'Aluno'

@admin.route("/responsavel")
@login_required
def responsavel():
    return 'Responsavel'