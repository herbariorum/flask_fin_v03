# application/admin/views.py
from flask import render_template, Blueprint, request, session, flash, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash
from datetime import date
from ..auth.views import login_required
from ..admin.formulario import FormProfile
from ..models import User
from .. import db

admin = Blueprint('admin', __name__)


@admin.route("/painel")
@login_required
def painel():
    return render_template('admin/painel.html', title = 'Finance')


@admin.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.filter_by(id=session['user_id']).first()
    form = FormProfile(request.form, obj=user)
    if request.method == 'POST' and form.validate():  
        user.username = form.username.data
        user.email = form.email.data
        user.password_hash = generate_password_hash(form.password_hash.data)
        user.updated_on = date.today() 
        try:
            db.session.commit()
            msg = 'Seus dados foram atualizados com sucesso'
            tipo = 'success'
        except SQLAlchemyError as e:
            msg = "Não foi possível atualizar os seus dados.\n O seguinte erro ocorreu: {}".format(e)
            tipo = 'error'
            db.session.rollback()
        else:
            flash(msg, tipo)
            return redirect(url_for('admin.painel'))
        flash(msg, tipo)
    return render_template('admin/profile.html', title='Finance', form=form)

@admin.route("/aluno")
@login_required
def aluno():
    return redirect(url_for('aluno.index'))

@admin.route("/responsavel")
@login_required
def responsavel():
    return redirect(url_for('responsavel.index'))

def gera_hash(password):
    return generate_password_hash(password)