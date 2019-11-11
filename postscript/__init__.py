import os

from flask import Flask, render_template, request
from .forms import csrf
from .models import db
from flask_migrate import Migrate

import jinja2

app = Flask(__name__)

app.config.from_object('config.Config')

db.init_app(app)
migrate = Migrate(app, db)
csrf.init_app(app)

from postscript import views

if __name__ == '__main__':
    app.run()