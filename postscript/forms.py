from flask_wtf import FlaskForm, CSRFProtect
from wtforms import IntegerField, StringField, TextAreaField
from wtforms.validators import DataRequired

csrf = CSRFProtect()

class MessageForm(FlaskForm):
    product_id = IntegerField('Product Id', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])

class SendForm(FlaskForm):
    phone = IntegerField('Phone', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
