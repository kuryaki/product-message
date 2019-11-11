# pylint: disable=missing-docstring,too-few-public-methods,invalid-name
import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

## Routes

@app.route('/', methods=['GET'])
def home():
    products = Product.query.limit(20).all()
    return render_template('home.html', products=products)

@app.route('/products', methods=['POST'])
def products():
    return 'Create Products'

@app.route('/products/<int:product_id>/messages', methods=['GET'])
def list_product_messages(product_id):
    return 'List product: %s messages' % product_id

@app.route('/products/<int:product_id>/messages', methods=['GET', 'POST'])
def add_message(product_id):
    return 'Create a product: %s message' % product_id

@app.route('/messages/<int:message_id>/send', methods=['POST'])
def send_message(message_id):
    return 'Send a Message'


## Models

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Product %r - %r>' % self.name, self.price

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