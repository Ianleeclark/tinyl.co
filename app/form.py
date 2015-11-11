from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class UrlForm(Form):
    link = StringField('link', validators=[DataRequired()])