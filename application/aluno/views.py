# application/aluno/views.py

from flask import render_template, Blueprint, request, url_for, flash, redirect, session, jsonify
from .formulario import FormAluno, FormSearch
from ..models import Aluno
from ..models import Responsavel
from ..auth.views import login_required
from flask_sqlalchemy import orm

from pyUFbr.baseuf import ufbr

aluno = Blueprint('aluno', __name__, template_folder='templates')


@aluno.route("/")
@login_required
def index():
    aluno = Aluno.query.all()
    # print('Alunos ', aluno)
    return render_template('aluno/index.html', title = "Finance", rows=aluno)


@aluno.route('<int:id>/view', methods=['GET'])
@login_required
def view(id):
    # aluno = Aluno.query.filter_by(id=id).first()
    # return render_template('view.html', title='Finance', row=aluno)
    return 'view'

@aluno.route('/new', methods=['GET','POST'])
@login_required
def new():
    form = FormAluno(request.form)
    # if request.method == 'POST':
    #     # se a sessão ainda não existe:
    #     if not session['id_pai']:    
    #         session['id_pai'] = request.args.get('id_pai') # se não existe retorna None    
    #         session['nome_pai'] = request.args.get('nome_pai')
        
        # if not session['id_mae']:
        #     session['id_mae'] = request.args.get('id_mae')
        #     session['nome_mae'] = request.args.get('nome_mae')


    return render_template('aluno/new.html', title='Finance', form=form)

@aluno.route('/search_responsavel', methods=['GET', 'POST'])
@login_required
def search_responsavel():
    form = FormSearch(request.form)
    msg = None
    tipo = None

    if request.method == 'POST':
        data = request.get_json()
        termo = data[0]
        responsavel = data[1]

        retorno = Responsavel.query.filter_by(tipo_responsavel = responsavel).filter(Responsavel.nome.like('%' + termo + '%')).all()

        row = retorno[0]

        row_as_dict = {"Data": []}        
        data_as_dict = {column: str(getattr(row, column)) for column in row.__table__.c.keys()}
        row_as_dict["Data"].append(data_as_dict) 
       
        return row_as_dict
    return render_template('aluno/search.html', title='Finance', form=form)

@aluno.route('/list_cities', methods=['GET'])
@login_required
def list_cities():
    uf = request.args.get('uf')
    return Convert(ufbr.list_cidades(uf))

def Convert(lst):
    res_dct = {lst[i]: lst[i] for i in range(0, len(lst), 2)}
    return res_dct

def limpa_item_da_sessao(key):
    [session.pop(key) for key in list(session.keys()) if key != 'flashes']