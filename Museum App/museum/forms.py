


from flask_wtf import FlaskForm
import re
from wtforms import StringField, PasswordField, SubmitField, BooleanField, Form, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
#from models import  *




class ArtPieceSearchForm(FlaskForm):
    choices = [('title', 'title')]
    select = SelectField('Search for art:', choices=choices)
    search = StringField('')
    submit = SubmitField('SUBMIT')



# class ItemSearchForm(FlaskForm):
#     choices = [('Video Games', 'Video Games'),('Mobile Phones', 'Mobile Phones')]
#     select = SelectField('Search for items:', choices=choices)
#     search = StringField('')
#     submit = SubmitField('SUBMIT')