


from flask_wtf import FlaskForm
import re
from wtforms import StringField, PasswordField, SubmitField, BooleanField, Form, SelectField, HiddenField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
#from models import  *




class ArtPieceSearchForm(FlaskForm):
    choices = [('title', 'title')]
    select = SelectField('Search for art:', choices=choices)
    search = StringField('')
    submit = SubmitField('SUBMIT')


# class QRScanForm(FlaskForm):
# 	scan = StringField('', render_kw={"placeholder": "QR Code"}, class_= "qrcode-text")
# 	photo = FileField('', validators=[FileRequired()], render_kw={"accept":"image/*", "capture":"environment", "onclick":"return showQRIntro();", "onchange":"openQRCamera(this);", "tabindex":"-1"})
# 	submit = SubmitField('Submit')

# class ItemSearchForm(FlaskForm):
#     choices = [('Video Games', 'Video Games'),('Mobile Phones', 'Mobile Phones')]
#     select = SelectField('Search for items:', choices=choices)
#     search = StringField('')
#     submit = SubmitField('SUBMIT')