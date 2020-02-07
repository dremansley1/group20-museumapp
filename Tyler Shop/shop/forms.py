from flask_wtf import FlaskForm
import re
from wtforms import StringField, PasswordField, SubmitField, BooleanField, Form, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from shop.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()]) # Regexp('^,{4,8}$', message='Your password should be between 4 and 8 characters long.')
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered.Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class CheckoutForm(FlaskForm):
    firstname = StringField('First Name:', validators=[DataRequired(), Length(min=3, max=15)])
    surname = StringField('Surname:', validators=[DataRequired(), Length(min=3, max=15)])
    address1 = StringField('Address Line 1:', validators=[DataRequired(), Length(min=5, max=30)])
    postcode = StringField('Postcode:', validators=[DataRequired(), Length(min=6, max=8)])

    nameoncard = StringField('Name on Card:', validators=[DataRequired(), Length(min=3, max=30)])
    cardnumber = StringField('Card Number:', validators=[DataRequired(), Length(min=16, max=16)])
    expirationdate = StringField('Expiration Date:', validators=[DataRequired(), Length(min=5, max=5)])
    cvvcode = StringField('CVV code:', validators=[DataRequired(), Length(min=3,max=3)])

    submit = SubmitField('Checkout Now')

    def validate_firstname(self, firstname):
        if firstname.data.isalpha() == False:
            raise ValidationError('First Name cannot contain any numbers.')

    def validate_surname(self, surname):
        if surname.data.isalpha() == False:
            raise ValidationError('Surname cannot contain any numbers.')

#DOES NOT CHECK PROPERLY FOR NUMBERS IN STRINGS


    def validate_cardnumber(self, cardnumber):
        if cardnumber.data.isdigit() == False:
            raise ValidationError('Card Number cannot contain any character other than numbers.')



class ItemSearchForm(FlaskForm):
    choices = [('Video Games', 'Video Games'),('Mobile Phones', 'Mobile Phones')]
    select = SelectField('Search for items:', choices=choices)
    search = StringField('')
    submit = SubmitField('SUBMIT')
