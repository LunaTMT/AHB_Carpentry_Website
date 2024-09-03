from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired



class PhotoForm(FlaskForm):
    name  = StringField('Property name', validators=[DataRequired()])
    photos = FileField('Upload Photos', validators=[FileAllowed(['jpg', 'png', 'jpg'], 'Images only!')], render_kw={"multiple": True})
    submit = SubmitField('Upload')

