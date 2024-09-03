
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
    first_name      = StringField('First Name', validators=[DataRequired()])
    last_name       = StringField('Last Name')
    email           = StringField('Email Address', validators=[DataRequired(), Email()])
    message         = TextAreaField('Message', validators=[DataRequired()])
    submit          = SubmitField('Submit')