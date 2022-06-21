# application/responsavel/views.py

from flask import render_template, Blueprint, request, url_for, flash, redirect
from datetime import date
from sqlalchemy.exc import SQLAlchemyError
from ..models import Responsavel
from ..auth.views import login_required
from .formulario import FormResponsavel
from pycpfcnpj import cpf
from ..auth.views import login_required
from ..filter.uteis import Uteis

from application import db



responsavel = Blueprint('responsavel', __name__)


@responsavel.route("/", methods=['GET', 'POST'])
def index():
    form = FormResponsavel(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        msg = None
        tipo = None
        nome = form.nome.data
        ccpf = form.cpf.data
        checkCpfValido = cpf.validate(ccpf)
        email = form.email.data
        sexo = form.sexo.data
        tipo_responsavel = form.tipo_responsavel.data
        profissao = form.profissao.data
        endereco = form.endereco.data
        contato = form.contato.data
        if not checkCpfValido:
            msg = "Entre com um cpf válido"
            tipo = "warning"
        check_Cpf_Exist = Responsavel.query.filter_by(cpf=Uteis.is_only_number(ccpf)).first()
        if check_Cpf_Exist:
            msg = "Este CPF já está cadastrado no sistema para {}".format(check_Cpf_Exist.nome)
            tipo = "warning"
        check_Email_Exist = Responsavel.query.filter_by(email=email).first()
        if check_Email_Exist:
            msg = "Este Email já está cadastrado no sistema para {}".format(check_Cpf_Exist.nome)
            tipo = "warning"
        if msg is None:
            try:
                responsavel = Responsavel(
                    nome = nome,
                    cpf = Uteis.is_only_number(ccpf),
                    email = email,
                    sexo = sexo,
                    tipo_responsavel = tipo_responsavel,
                    profissao = profissao,
                    endereco = endereco,
                    contato = contato,
                    created_on = date.today()
                )
                db.session.add(responsavel)
                db.session.commit()
                msg = "O registro foi cadastrado com sucesso"
                tipo = 'success'
            except SQLAlchemyError as e:
                db.session.rollback()
                msg = "Não foi possível incluir o registro.\n O seguinte erro ocorreu: {}".format(e)
                tipo = 'error'
            else:
                flash(msg, tipo)
                return redirect(url_for('responsavel.index'))
        flash(msg, tipo)
    return render_template('responsavel/index.html', title = "Finance", form=form)

