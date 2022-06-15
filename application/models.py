from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import re
from application import db
import json



class User(db.Model):
    __tablename__ = 'users_table'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(40), unique=True, nullable=True)
    password_hash = db.Column(db.String(128))
    created_on = db.Column(db.Date, default=datetime.date.today())
    updated_on = db.Column(db.Date)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def check_password_strength_and_hash_if_ok(password):
        if len(password) < 8:
            return 'A senha é muito curta'
        if len(password) > 32:
            return 'A senha é muito longa'
        if re.search(r'[A-Z]', password) is None:
            return 'A senha deve incluir pelo menos uma letra maiúscula'
        if re.search(r'[a-z]', password) is None:
            return 'A senha deve incluir pelo menos uma letra minúscula'
        if re.search(r'\d', password) is None:
            return 'A senha deve incluir pelo menos um número'
        if re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None:
            return 'A senha deve incluir pelo menos um simbolo'
        return ''

class Aluno(db.Model):
    __tablename__ = 'alunos_table'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo = db.Column(db.String(100))
    nome = db.Column(db.String(80), nullable=False)
    cpf = db.Column(db.String(11), unique=True)
    rg = db.Column(db.String(15))
    orgao_exp_rg = db.Column(db.String(15))
    uf_exp_rg = db.Column(db.String(2))
    nascimento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.Integer)
    pai = db.Column(db.Integer)
    mae = db.Column(db.Integer)
    endereco = db.Column(db.String(255))
    bairro = db.Column(db.String(80))
    cidade = db.Column(db.String(8))
    uf = db.Column(db.String(2))
    
    uf_naturalidade = db.Column(db.String(2))
    naturalidade = db.Column(db.String(30))
    nacionalidade = db.Column(db.String(20))
    certidao_nascimento = db.Column(db.String(10))
    termo_certidao_nasc = db.Column(db.String(10))
    folha_certidao_nasc = db.Column(db.String(10))
    livro_certidao_nasc = db.Column(db.String(10))
    data_emissao_certidao = db.Column(db.Date)
    # cartorio_certidao = db.Column(db.String(30))

    matricula = db.Column(db.String(32))

    status = db.Column(db.SmallInteger(), default=1)

    created_on = db.Column(db.Date, default=datetime.date.today())
    updated_on = db.Column(db.Date)


class Responsavel(db.Model):
    __tablename__ = 'responsavel_table'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), nullable=False)
    sexo = db.Column(db.Integer)
    cpf = db.Column(db.String(11), unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    tipo_responsavel = db.Column(db.Integer)
    profissao = db.Column(db.String(80))
    contato = db.Column(db.String(11))
    endereco = db.Column(db.String(255))
    status = db.Column(db.SmallInteger(), default=1)
    created_on = db.Column(db.Date, default=datetime.date.today())
    updated_on = db.Column(db.Date)


