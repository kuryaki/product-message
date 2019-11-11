# pylint: disable=missing-docstring,too-few-public-methods,invalid-name
import os

from flask import Flask, render_template, request

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import IntegerField, StringField, TextAreaField
from wtforms.validators import DataRequired

from twilio.rest import Client

import jinja2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['TWILIO_SID'] = 'AC34af70a5b417bc6701280bf0222462af'
app.config['TWILIO_TOKEN'] ='e03dc9262712600f85a0dcda30c61101'
app.config['TWILIO_MESSAGING_SERVICE'] = 'MG95a674c87cf3664036c1f292cafb30f9'

csrf = CSRFProtect()
csrf.init_app(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

client = Client(app.config['TWILIO_SID'], app.config['TWILIO_TOKEN'])

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
            twilio_message = client.messages.create(
                messaging_service_sid=app.config['TWILIO_MESSAGING_SERVICE'],
                to='+1' + request.form['phone'], 
                body=request.form['content'])
            print(twilio_message)


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