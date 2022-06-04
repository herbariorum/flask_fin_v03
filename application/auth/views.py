# application/auth/views.py
import functools
import re
from flask import (
    render_template, 
    Blueprint, request, 
    redirect, 
    url_for,flash,
    session, g
    )
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError
from .form import FormLogin, FormRegister
from ..models import User
from .. import db

auth = Blueprint('auth', __name__, template_folder='templates')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not 'email' in session.keys():
            return redirect("/auth/login")
        return view(**kwargs)
    return wrapped_view

@auth.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = (
            User.query.filter_by(id=user_id).first()
        )

@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = FormLogin(request.form)
    msg = None
    tipo = None
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password_hash = form.password_hash.data
        try:
            user = User.query.filter_by(email=email).first()
            if user is None:
                msg = "O Email não existe na base de dados"
                tipo = 'warning'
            elif not user.verify_password(password_hash):
                msg = "Senha incorreta"
                tipo = 'warning'
            if msg is None:
                session.clear()
                session['user_id'] = user.id
                session['username'] = abrevia_nome(user.username) 
                session['email'] = user.email
                msg = 'Usuário cadastrado com sucesso'
                tipo = 'success'
                return redirect(url_for('admin.painel'))
        except SQLAlchemyError as e:
            msg = "Não foi possível fazer login.\n O seguinte erro ocorreu: {}".format(e)
            tipo = 'error'
            db.session.rollback()        
        flash(msg, tipo)
    return render_template('auth/login.html', title='Finance', form=form)


@auth.route("/register", methods=['GET', 'POST'])
@login_required
def register():
    form = FormRegister(request.form)
    msg = None
    tipo = None
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password_hash = generate_password_hash(form.password_hash.data)
        
        try:
            user = User.query.filter_by(email=email).first()
            if user:
                msg = "O Email já existe na base de dados"
                tipo = 'warning'
            if msg is None:
                user = User(
                    username = username,
                    email = email,
                    password_hash = password_hash
                )
                db.session.add(user)
                db.session.commit()
                msg = 'Usuário cadastrado com sucesso'
                tipo = 'success'
                return redirect(url_for('admin.painel'))
        except SQLAlchemyError as e:
            msg = "Não foi possível cadastrar o novo usuário.\n O seguinte erro ocorreu: {}".format(e)
            tipo = 'error'
            db.session.rollback()        
        flash(msg, tipo)
    return render_template('auth/register.html', title='Finance', form=form)

@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def gera_hash(password):
    return generate_password_hash(password)
    
# Créditos:
# https://acervolima.com/python-imprime-as-iniciais-de-um-nome-com-o-sobrenome-por-extenso/
def abrevia_nome(s):
    l = s.split()
    new = ""
    for i in range(len(l)-1):
        s = l[i]
        new += (s[0].upper()+'.')
    new += l[-1].title()
    return new