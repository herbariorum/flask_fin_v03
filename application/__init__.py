# https://www.patricksoftwareblog.com/using-blueprints-to-organize-your-application/

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


def page_not_found(e):
    return render_template('404.html'), 404

def method_not_allowed(e):
    return render_template('405.html'), 405

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_pyfile('../config.py')

    db.init_app(app)
    from application.admin.views import admin
    from application.auth.views import auth
    from application.aluno.views import aluno
    from application.responsavel.views import responsavel


    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(aluno, url_prefix='/aluno')
    app.register_blueprint(responsavel, url_prefix='/responsavel')

    @app.route('/')
    @app.route('/index')
    def index():
        return redirect(url_for('admin.painel'))

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)

    return app