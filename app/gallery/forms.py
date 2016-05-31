from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import Length, DataRequired
from wtforms import ValidationError
from flask_wtf.file import FileField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Category


# class ImageForm(Form):
#     name = StringField('Image Name', validators=[Length(1, 64)])
#     tag = IntegerField('Tag Value', default=50, validators=[DataRequired(), Length(1, 64)])
#     image = FileField('Your photo')
#     submit = SubmitField('Upload Image')

def enabled_categories():
    return Category.query.all()


class CategoryForm(Form):
    name = StringField('New Album Name', validators=[Length(1, 64)])
    submit = SubmitField('Add Album')


class ImageForm(Form):
    name = StringField('Name', validators=[Length(1, 64)])
    category = QuerySelectField(query_factory=enabled_categories, get_label='name', allow_blank=True,
                                validators=[DataRequired()])

    @classmethod
    def category_choice(cls):
        choices = [(x.id, str(x.name)) for x in Category.query.all()]
        cls.lazy_value = choices

    image = FileField('Your photo', validators=[DataRequired(), DataRequired()])
    submit = SubmitField('Upload')


class SwitchAlgorithmForm(Form):
    text = StringField('The context of watermark')
    type = SelectField('Watermark Type', choices=[('visible_mark', 'visible'), ('invisible_mark', 'invisible'),
                                                  ('print_watermark', 'print-watermark')])
    submit = SubmitField("Go")


class InvisibleForm(Form):
    text = StringField('The context of watermark')
    type = SelectField('Invisible Watermark Algorithm', choices=[('lsb', 'LSB algorithm'), ('qim', 'QIM algorithm'),
                                                                 ('dft', 'Discrete Fourier Transform')])
    submit = SubmitField("Process")
