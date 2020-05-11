from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, ValidationError
from flask_mail import Message, Mail
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired
import os, os.path

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or "postgresql://postgres:top2541top@localhost:5432/db_work"
app.config['SECRET_KEY'] = 'password'
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'bunnasorn.k@ku.th'
app.config["MAIL_PASSWORD"] = 'Top2541Top.'

db = SQLAlchemy(app)
mail = Mail()
mail.init_app(app)

class workForm(FlaskForm):
    name = StringField('Work name', validators=[DataRequired()])
    url = StringField('Work url', validators=[DataRequired()])
    desc = StringField('Work description')
    submit = SubmitField('Submit')

class contactForm(FlaskForm):
    subject = StringField('Subject *',  [validators.Required("Please enter your name.")])
    name = StringField('Name *',  [validators.Required("Please enter your name.")])
    email = StringField('Email *', validators=[DataRequired(), validators.Email()])
    msg = StringField('Message *', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Submit')

class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    url = db.Column(db.String())
    desc = db.Column(db.String())

    def __repr__(self):
        return '<work #{}: {}>'.format(self.id, self.name)

@app.route('/')
def index():
    works = Work.query.all()
    return render_template('index.html', works=works)

@app.route('/work/<id>')
def work(id):
    work = Work.query.get(id)
    return render_template('work.html', work=work)

@app.route('/add', methods=['POST', 'GET'])
def add():
    form = workForm()

    if form.validate_on_submit():
        work = Work(name=form.name.data, url=form.url.data, desc=form.desc.data)
        db.session.add(work)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add.html', form=form)

@app.route('/contact', methods=['POST', 'GET'])
def contact():
    form = contactForm()

    if form.validate_on_submit():
        msg = Message(form.subject.data, sender=form.email.data, recipients=['bunnasorn.k@ku.th, top2541top@gmail.com'])
        msg.body = """
        From: {} <{}>
        {}
        """ .format(form.name.data, form.email.data, form.msg.data)
        mail.send(msg)
        return redirect(url_for('index'))

    return render_template('contact.html', form=form)