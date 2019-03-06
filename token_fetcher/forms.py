from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired
from wtforms.fields.html5 import URLField

class AuthCodeForm(FlaskForm):
    # client_id = StringField('Client ID', validators=[InputRequired()])
    # redirect_uri = URLField('Redirect URI', validators=[InputRequired()])
    scope = StringField('Scope', validators=[InputRequired()])
    response_type = StringField('Response Type', validators=[InputRequired()])
    # state = StringField('State', validators=[InputRequired()])
