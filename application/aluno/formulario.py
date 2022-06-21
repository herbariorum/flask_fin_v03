from email.policy import default
from flask import session
import wtforms
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional
from flask_wtf import FlaskForm
from datetime import timedelta

estados = [
        ('AC', 'ACRE'),
        ('AL', 'ALAGOAS'),
        ("AM", "AMAZONAS"),
        ("AP", "AMAPÁ"),
        ("BA", "BAHIA"),
        ("CE", "CEARÁ"),
        ("DF", "DISTRITO FEDERAL"),
        ("ES", "ESPIRITO SANTO"),
        ("GO", "GOIÁS"),
        ("MA", "MARANHÃO"),
        ("MG", "MINAS GERAIS"),
        ("MS", "MATO GROSSO DO SUL"),
        ("MT", "MATO GROSSO"),
        ("PA", "PARÁ"),
        ("PB", "PARAÍBA"),
        ("PE", "PERNAMBUCO"),
        ("PI", "PIAUI"),
        ("PR", "PARANÁ"),
        ("RJ", "RIO DE JANEIRO"),
        ("RN", "RIO GRANDE DO NORTE"),
        ("RO", "RONDÔNIA"),
        ("RR", "RORAIMA"),
        ("RS", "RIO GRANDE DO SUL"),
        ("SC", "SANTA CATARINA"),
        ("SP", "SÃO PAULO"),
        ("SE", "SERGIPE"),
        ("TO", "TOCANTINS")
        ]

class FormAluno(FlaskForm):   

    nome = wtforms.StringField('Nome do Aluno', validators=[DataRequired(message="O campo é requerido"), Length(min=6, max=80, message="O campo deve ter entre 6 e 80 caracteres")])
    cpf = wtforms.StringField('CPF', validators=[DataRequired(message="O campo é requerido"), Length(min=11, max=18, message="O campo deve ter no mínimo 11 caracteres")])
    rg = wtforms.StringField('RG')
    orgao_exp_rg = wtforms.StringField('Órgão Emissor RG')
    uf_exp_rg = wtforms.SelectField(
        'UF',
        choices= estados, coerce=str, validate_choice=False
    )
    nascimento = wtforms.DateField('Data Nascimento')
    sexo = wtforms.SelectField(
        'Sexo',
        choices=(
            (0, 'Masculino'),
            (1, 'Feminino')
        ), coerce=int, validate_choice=False
    )
    pai = wtforms.StringField('Nome do Pai/Responsável', render_kw={'readonly': 'readonly'})
    mae = wtforms.StringField('Nome da Mãe/Responsável', render_kw={'readonly': 'readonly'})

    endereco = wtforms.StringField('Endereço')
    bairro = wtforms.StringField('Bairro')    
    uf = wtforms.SelectField(
        'UF',
        choices=estados, validate_choice=False
    )
    cidade = wtforms.SelectField('Cidade', choices=[], validate_choice=False)

    uf_naturalidade = wtforms.SelectField(
        'UF',
        choices=estados, validate_choice=False
    )
    naturalidade = wtforms.SelectField('Naturalidade', choices=[], validate_choice=False)
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

# class FormCidade(FlaskForm):
#     uf = wtforms.SelectField('UF', choices= estados)

#     nome = wtforms.SelectField('Cidade', choices= [])
#     submit = wtforms.SubmitField('Submit')