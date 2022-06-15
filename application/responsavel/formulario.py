
import wtforms
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf import FlaskForm
from pyUFbr.baseuf import ufbr


class FormResponsavel(FlaskForm):   

    nome = wtforms.StringField('Nome do Pai/Mãe/Responsável', validators=[DataRequired(message="O campo é requerido"), Length(min=6, max=80, message="O campo deve ter entre 6 e 80 caracteres")])
    cpf = wtforms.StringField('CPF', validators=[DataRequired(message="O campo é requerido"), Length(min=11, max=18, message="O campo deve ter no mínimo 11 caracteres")])
    sexo = wtforms.SelectField(
        'Sexo',
        choices=(
            (0, 'Masculino'),
            (1, 'Feminino')
        ), coerce=int
    )
    email = wtforms.EmailField('Email', validators=[Email(message="O campo é requerido")])
    tipo_responsavel = wtforms.SelectField(
        'Tipo de Responsável',
        choices=(
            (0, 'Pai'),
            (1, 'Mãe'),
            (2, 'Tutor Legal'),
            (3, 'Outros')
        )
    )
    profissao = wtforms.StringField('Profissão')
    contato = wtforms.StringField('Contato', validators=[DataRequired(message="O campo é requerido"), Length(min=9, max=11, message="O campo deve ter no mínimo 9 caracteres")])
    endereco = wtforms.StringField('Endereço Completo')


    submit = wtforms.SubmitField('Inserir')