import os
from flask import Flask, render_template, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired



basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY']='oursecretkey'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class Record(db.Model):
    __tablename__="record"

    id= db.Column(db.Integer)
    name= db.Column(db.Text)
    email= db.Column(db.Text)
    number= db.Column(db.Integer, primary_key=True)
    address= db.Column(db.Text)

    def __init__(self, name, email, number, address):
        self.name=name
        self.email=email
        self.number=number
        self.address=address

    def __repr__(self):
        return f"Company {self.id}: name={self.name}  email={self.email} number={self.number} address={self.address}"


class AddForm(FlaskForm):
    name = StringField("Enter Company Name: ")
    email = StringField("Enter Company Email: ")
    number = IntegerField("Enter Company Phone Number: ")
    address = StringField("Enter Company Address: ")
    submit = SubmitField("Add Company")

class DelForm(FlaskForm):
    number = IntegerField("Enter phone number of company to remove")
    submit = SubmitField("Remove Company")



db.create_all()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():

    form = AddForm()

    if form.validate_on_submit():

        name = form.name.data
        email = form.email.data
        number = form.number.data
        address = form.address.data
        new_record = Record(name, email, number, address)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('display'))

    return render_template('add.html', form=form)


@app.route('/display')
def display():

    record = Record.query.all()
    return render_template('display.html', record=record)


@app.route('/delete', methods=['GET', 'POST'])
def delete():

    form = DelForm()

    if form.validate_on_submit():
        number = form.number.data
        record = Record.query.get(number)
        db.session.delete(record)
        db.session.commit()
        return redirect('/display')

    return render_template('delete.html', form=form)
    


if __name__ == '__main__':
    app.run(debug=True)
