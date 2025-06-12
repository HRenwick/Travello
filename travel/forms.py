from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, FloatField
from wtforms.validators import InputRequired, Email, EqualTo

# Create Destination
class DestinationForm(FlaskForm):
    city_name = StringField('City', validators=[InputRequired('Please enter a city.')])
    country_name = StringField('Country', validators=[InputRequired('Please enter a country.')])
    description = TextAreaField('Description', validators=[InputRequired('Please enter a description.')])
    file_format = ['png', 'jpg', 'jpeg', 'webp']
    image = FileField('Destination Image', validators=[FileAllowed(file_format, 'Only JPG, WEBP or PNG file formats are accepted.')])
    exchange_rate = FloatField('Exchange Rate', validators=[InputRequired('Please enter an exchange rate.')])
    currency_code = SelectField('Currency', validators=[InputRequired('Please select a currency.')], 
                                choices=[('EUR'), ('CAD'), ('CHF'), ('CZK'), ('DKK'), ('GBP'), ('INR'), 
                                         ('JPY'), ('NZD'), ('PLN'), ('SGD'), ('THB'), ('USD'), ('VND')])
    submit = SubmitField('Create')

# Log In User
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('Please enter a username.')])
    password = PasswordField('Password', validators=[InputRequired('Please enter a password.')])
    submit = SubmitField('Log In')

# Sign Up User
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('Please enter a username.')])
    email = StringField('Email Address', validators=[InputRequired('Please enter an email.'), 
                                                          Email('Please enter a valid email.')])
    password = PasswordField('Password', validators=[InputRequired('Please enter a password.')])
    confirm = PasswordField('Confirm Password', validators=[EqualTo('password', message='Passwords must match.')])
    user_type = SelectField('User Type', choices=[('guest', 'Guest'), ('admin', 'Administrator')])
    submit = SubmitField('Sign Up')
    
# User Comments
class CommentForm(FlaskForm):
    text = TextAreaField('Post a comment', [InputRequired('Please enter your comment.')])
    submit = SubmitField('Create')