from flask import session
import wtforms
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf import FlaskForm
from wtforms.csrf.session import SessionCSRF
from datetime import timedelta
from config import SECRET_KEY
from pyUFbr.baseuf import ufbr


class FormAluno(FlaskForm):   

    nome = wtforms.StringField('Nome do Aluno', validators=[DataRequired(message="O campo é requerido"), Length(min=6, max=80, message="O campo deve ter entre 6 e 80 caracteres")])
    cpf = wtforms.StringField('CPF', validators=[DataRequired(message="O campo é requerido"), Length(min=11, max=18, message="O campo deve ter no mínimo 11 caracteres")])
    rg = wtforms.StringField('RG')
    orgao_exp_rg = wtforms.StringField('Órgão Emissor RG')
    uf_exp_rg = wtforms.SelectField(
        'UF',
        choices=ufbr.list_uf
    )
    nascimento = wtforms.DateField('Data Nascimento', validators=[DataRequired(message="O campo é requerido")])
    sexo = wtforms.SelectField(
        'Sexo',
        choices=(
            (0, 'Masculino'),
            (1, 'Feminino')
        ), coerce=int
    )
    pai = wtforms.StringField('Nome do Pai/Responsável', render_kw={'readonly': 'readonly'})
    mae = wtforms.StringField('Nome da Mãe/Responsável', render_kw={'readonly': 'readonly'})

    endereco = wtforms.StringField('Endereço')
    bairro = wtforms.StringField('Bairro')    
    uf = wtforms.SelectField(
        'UF',
        choices=ufbr.list_uf
    )
    cidade = wtforms.SelectField('Cidade')

    uf_naturalidade = wtforms.SelectField(
        'UF',
        choices=ufbr.list_uf
    )
    naturalidade = wtforms.SelectField('Naturalidade')
    nacionalidade = wtforms.StringField('Nacionalidade')

    certidao_nascimento = wtforms.StringField('Certidão')
    termo_certidao_nasc = wtforms.StringField('Termo')
    folha_certidao_nasc = wtforms.StringField('Folha')
    livro_certidao_nasc = wtforms.StringField('Livro')
    data_emissao_certidao = wtforms.DateField('Data Emissão')

    matricula = wtforms.StringField('Matrícula')

    status = wtforms.BooleanField('Status')
    submit = wtforms.SubmitField('Inserir')


class FormSearch(FlaskForm):
    termo = wtforms.StringField('Termo para pesquisa', validators=[DataRequired(message="O campo é requerido")])
    submit = wtforms.SubmitField('Pesquisar')