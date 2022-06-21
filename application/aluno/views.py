# application/aluno/views.py
from datetime import date
from pycpfcnpj import cpf
from flask import Response, render_template, Blueprint, request, url_for, flash, redirect, session, jsonify
from sqlalchemy import false, true
from sqlalchemy.exc import SQLAlchemyError

from config import PER_PAGE
from .formulario import FormAluno, FormSearch
from ..models import Aluno, Cidades
from ..models import Responsavel, responsaveis_schema
from ..auth.views import login_required
from application import db
from ..filter.uteis import Uteis

from pyUFbr.baseuf import ufbr


aluno = Blueprint('aluno', __name__, template_folder='templates')


@aluno.route("/", defaults={"page": 1}, methods=['GET', 'POST'])
@aluno.route("/index/", defaults={"page": 1}, methods=['GET', 'POST'])
@aluno.route("/index/<int:page>", methods=['GET', 'POST'])
@login_required
def index(page): 
    if request.method == 'POST':
        termo = request.values.get('termo-busca')
        search = "%{}%".format(termo)
        aluno =  Aluno.query.order_by(Aluno.id.asc()).filter(Aluno.nome.like(search)).paginate(page, per_page=PER_PAGE, error_out=True)
        return render_template('aluno/index.html', title = "Finance", rows=aluno)

    aluno = Aluno.query.order_by(Aluno.id.asc()).paginate(page=page, per_page=PER_PAGE, error_out=True)
    return render_template('aluno/index.html', title = "Finance", rows=aluno)

@aluno.route('<int:id>/view', methods=['GET'])
@login_required
def view(id):
    aluno = Aluno.query.filter_by(id=id).first()
    return render_template('aluno/view.html', title='Finance', row=aluno)

@aluno.route('/new', methods=['GET','POST'])
@login_required
def new():
    form = FormAluno(request.form)
    form.naturalidade.choices = [(cidade.id, cidade.nome) for cidade in Cidades.query.filter_by(uf='TO').all()]
    form.cidade.choices = [(cidade.id, cidade.nome) for cidade in Cidades.query.filter_by(uf='TO').all()]
    if request.method == 'POST':
        msg = None
        tipo = None

        nome = form.nome.data
        ccpf = form.cpf.data
        checkCpfValido = cpf.validate(ccpf)
        if not checkCpfValido:
            msg = 'Entre com um cpf válido'
            tipo = 'warning'
        check_Cpf_Exist = Aluno.query.filter_by(cpf=Uteis.is_only_number(ccpf)).first() 
        if check_Cpf_Exist:
            msg = "Este CPF já está cadastrado no sistema para {}".format(check_Cpf_Exist.nome)
            tipo = 'warning' 
        sexo = form.sexo.data
        data_nasc = form.nascimento.data
        rg = form.rg.data
        org_exp_rg = form.orgao_exp_rg.data
        uf_exp_rg = form.uf_exp_rg.data
        uf_naturalidade = form.uf_naturalidade.data
        cidade_naturalidade = form.naturalidade.data
        nacionalidade = form.nacionalidade.data
        pai = form.pai.data
        mae = form.mae.data
        endereco = form.endereco.data
        bairro = form.bairro.data
        uf = form.uf.data
        cidade = form.cidade.data
        # ----------------------------
        matricula_aluno = ''
        certidao = ''
        termo = ''
        folha = ''
        livro = ''
        data_emissao = ''
        # ----------------------------
        request_tipo_certidao = request.values.get('tipo_certidao')
        if request_tipo_certidao == '0' or request.values.get('tipo_certidao') is None:
            msg = 'Selecione o tipo de certidão de nascimento'
            tipo = 'warning'
        elif request_tipo_certidao == '1':
            matricula_aluno = form.matricula.data
        else:
            certidao = form.certidao_nascimento.data
            termo = form.termo_certidao_nasc.data
            folha = form.folha_certidao_nasc.data
            livro = form.livro_certidao_nasc.data
            data_emissao = form.data_emissao_certidao.data
        if msg is None:
            try:    
                if request_tipo_certidao == '1':          
                    aluno = Aluno(
                        nome = nome,
                        cpf = Uteis.is_only_number(ccpf),
                        sexo = sexo,
                        nascimento = data_nasc,
                        rg = rg,
                        orgao_exp_rg = org_exp_rg,
                        uf_exp_rg = uf_exp_rg,
                        uf_naturalidade = uf_naturalidade,
                        naturalidade = cidade_naturalidade,
                        nacionalidade = nacionalidade,
                        pai = pai,
                        mae = mae,
                        endereco = endereco,
                        cidade = cidade,
                        bairro = bairro,
                        uf = uf,
                        matricula = matricula_aluno               
                    )
                else:
                    aluno = Aluno(
                        nome = nome,
                        cpf = Uteis.is_only_number(ccpf),
                        sexo = sexo,
                        nascimento = data_nasc,
                        rg = rg,
                        orgao_exp_rg = org_exp_rg,
                        uf_exp_rg = uf_exp_rg,
                        uf_naturalidade = uf_naturalidade,
                        naturalidade = cidade_naturalidade,
                        nacionalidade = nacionalidade,
                        pai = pai,
                        mae = mae,
                        endereco = endereco,
                        cidade = cidade,
                        bairro = bairro,
                        uf = uf,                       
                        certidao_nascimento = certidao,
                        termo_certidao_nasc = termo,
                        folha_certidao_nasc = folha,
                        livro_certidao_nasc = livro,
                        data_emissao_certidao = data_emissao
                    )
                db.session.add(aluno)
                db.session.commit()
                msg = "O registro foi cadastrado com sucesso"
                tipo = 'success'
            except SQLAlchemyError as e:
                db.session.rollback()
                msg = "Não foi possível incluir o registro.\n O seguinte erro ocorreu: {}".format(e)
                tipo = 'error'
            else:
                flash(msg, tipo)
                return redirect(url_for('aluno.index'))
        flash(msg, tipo)
       
    return render_template('aluno/new.html', title='Finance', form=form)
    

@aluno.route('/cidade/<uf>')
def cidade(uf):
    cidades = Cidades.query.filter_by(uf=uf).all()
    cidadeArray = []
    for cidade in cidades:
        cidadeObj = {}
        cidadeObj['id'] = cidade.id
        cidadeObj['nome'] = cidade.nome
        cidadeArray.append(cidadeObj)

    return jsonify({'cidades': cidadeArray})

# Rota responsavel pela busca de responsavel
# parametros: termo de busca, tipo de responsavel - passados via javascript
# retorno: id, nome, cpf, e tipo de responsavel no formato json
@aluno.route('/search_responsavel', methods=['GET', 'POST'])
@login_required
def search_responsavel():
    form = FormSearch(request.form)
    if request.method == 'POST':
        data = request.get_json()
        termo = data[0]
        responsavel = data[1]

        retorno = Responsavel.query.filter_by(tipo_responsavel = responsavel).filter(Responsavel.nome.like('%' + termo + '%')).all()
        output = responsaveis_schema.dump(retorno)

        return jsonify(output)
    return render_template('aluno/search.html', title='Finance', form=form)

@aluno.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):    
    aluno = Aluno.query.filter_by(id=id).first()    
    if aluno:
        try:
            db.session.delete(aluno)
            db.session.commit()            
            return jsonify(result="success") 
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify(result="error")


# lista todas as cidades por estado
# parametro: uf
# retorno: dicionario formato {'Augustinopolis':'Augustinopolis'}
@aluno.route('/list_cities', methods=['GET'])
@login_required
def list_cities():
    uf = request.args.get('uf')
    return Convert(ufbr.list_cidades(uf))

# função usada pela rota list_cities
def Convert(lst):
    res_dct = {lst[i]: lst[i] for i in range(0, len(lst), 2)}
    return res_dct