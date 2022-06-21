import wtforms
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf import FlaskForm


class FormProfile(FlaskForm):
    username = wtforms.StringField('Nome do Usuário', validators=[DataRequired(message="O campo é requerido"), Length(min=6, message="O campo deve ter no mínimo 6 caracteres")])
    email = wtforms.EmailField('Email', validators=[DataRequired(message="O campo é requerido"), Email(message="Endereço de email inválido")])
    password_hash = wtforms.PasswordField('Password', validators=[DataRequired(message="O campo é requerido"), Length(min=6, message="O campo deve ter no mínimo 6 dígitos"), EqualTo('confirm', message='As senhas devem corresponder')])
    confirm  = wtforms.PasswordField('Repita a senha')   
    submit = wtforms.SubmitField('Alterar')