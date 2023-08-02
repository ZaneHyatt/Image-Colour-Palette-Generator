from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms.validators import DataRequired
from wtforms import IntegerField, validators, SelectField

class UploadImg(FlaskForm):
    file = FileField(validators=[DataRequired()])
    count = SelectField(u'Colour count', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')])