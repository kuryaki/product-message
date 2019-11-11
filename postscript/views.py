from . import app
from flask import Blueprint, render_template, request
from .models import db, Product, Message
from .forms import MessageForm, SendForm
from twilio.rest import Client
import jinja2

views = Blueprint('views', __name__)
client = Client(app.config['TWILIO_SID'], app.config['TWILIO_TOKEN'])   

@app.route('/', methods=['GET'])
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@app.route('/products/<int:product_id>/messages', methods=['GET', 'POST'])
def product_messages(product_id):
    messageForm = MessageForm()

    if request.method == 'POST':
        if messageForm.validate():
            message = Message(
                    name=request.form['name'], 
                    product_id=request.form['product_id'], 
                    content=request.form['content']
                )
            db.session.add(message)
            db.session.commit()

    products = Product.query.all()
    selected_product = Product.query.filter_by(id=product_id).first()
    messages = Message.query.filter_by(product_id=product_id).all()

    return render_template(
            'home.html', 
            messageForm=messageForm, 
            products=products, 
            selected_product=selected_product, 
            messages=messages
        )

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

    return render_template(
            'home.html', 
            sendForm=sendForm, 
            messageForm=messageForm, 
            products=products, 
            selected_product=selected_product, 
            messages=messages, 
            selected_message=selected_message, 
            message_content=message_content
        )