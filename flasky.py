import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'chave-secreta-avaliacao-semestral')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


# Modelo do Banco de Dados
class Curso(db.Model):
    __tablename__ = 'cursos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'<Curso {self.nome}>'


# Formulário de Cadastro de Cursos
class CursoForm(FlaskForm):
    nome = StringField(
        'Qual é o nome do curso?',
        validators=[DataRequired(), Length(max=100)]
    )
    descricao = TextAreaField(
        'Descrição (250 caracteres)',
        validators=[DataRequired(), Length(max=250)]
    )
    submit = SubmitField('Cadastrar')


# Rota Principal
@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())


# Rota de Cadastro e Listagem de Cursos
@app.route('/cursos', methods=['GET', 'POST'])
def cursos():
    form = CursoForm()
    if form.validate_on_submit():
        novo_curso = Curso(
            nome=form.nome.data.strip(),
            descricao=form.descricao.data.strip()
        )
        db.session.add(novo_curso)
        db.session.commit()
        flash('Curso cadastrado com sucesso!')
        return redirect(url_for('cursos'))

    lista_cursos = Curso.query.all()
    return render_template('cursos.html', form=form, cursos=lista_cursos)


# Tratamento de Erros (captura as rotas não criadas como /professores, /ocorrencias, etc.)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# Garante a criação automática da tabela no SQLite ao iniciar a aplicação
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)