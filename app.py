# pylint: disable=missing-docstring,too-few-public-methods,invalid-name
import os

from flask import Flask, render_template, request

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import IntegerField, StringField, TextAreaField
from wtforms.validators import DataRequired

import jinja2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'you-will-never-guess'

csrf = CSRFProtect()
csrf.init_app(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

## Forms

class MessageForm(FlaskForm):
    product_id = IntegerField('Product Id', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])

class SendForm(FlaskForm):
    phone = IntegerField('Phone', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])

## Routes

@app.route('/', methods=['GET'])
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@app.route('/products', methods=['POST'])
def products():
    return 'Create Products'

@app.route('/products/<int:product_id>/messages', methods=['GET', 'POST'])
def product_messages(product_id):
    messageForm = MessageForm()

    if request.method == 'POST':
        if messageForm.validate():
            message = Message(name=request.form['name'], product_id=request.form['product_id'], content=request.form['content'])
            db.session.add(message)
            db.session.commit()

    products = Product.query.all()
    selected_product = Product.query.filter_by(id=product_id).first()
    messages = Message.query.filter_by(product_id=product_id).all()

    return render_template('home.html', messageForm=messageForm, products=products, selected_product=selected_product, messages=messages)

@app.route('/messages/<int:message_id>/send', methods=['GET', 'POST'])
def send_message(message_id):

    sendForm = SendForm()
    messageForm = MessageForm()

    if request.method == 'POST':
        if sendForm.validate():
            print('Send to Twilio')
            print(request.form['phone'])
            print(request.form['content'])


    products = Product.query.all()
    selected_message = Message.query.filter_by(id=message_id).first()
    selected_product = Product.query.filter_by(id=selected_message.product_id).first()
    messages = Message.query.filter_by(product_id=selected_message.product_id).all()

    message_template = jinja2.Template(selected_message.content)
    message_content = message_template.render({ 'product': vars(selected_product) })

    return render_template('home.html', sendForm=sendForm, messageForm=messageForm, products=products, selected_product=selected_product, messages=messages, selected_message=selected_message, message_content=message_content)


## Models

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.name

class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.Text)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return '<Message %r>' % self.name

if __name__ == '__main__':
    app.run()