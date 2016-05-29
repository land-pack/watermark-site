from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import  Length, DataRequired
from wtforms import ValidationError
from flask_wtf.file import FileField


class ImageForm(Form):
    name = StringField('Image Name', validators=[Length(1, 64)])
    tag = IntegerField('Tag Value', default=50, validators=[DataRequired(), Length(1, 64)])
    image = FileField('Your photo')
    submit = SubmitField('Upload Image')