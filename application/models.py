from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from application import db

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



class Aluno(db.Model):
    __tablename__ = 'alunos_table'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), nullable=False)
    cpf = db.Column(db.String(11))
    nascimento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(10))
    status = db.Column(db.SmallInteger(), default=1)
    created_on = db.Column(db.Date, default=datetime.date.today())
    updated_on = db.Column(db.Date)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'nascimento': self.nascimento,
            
        }
