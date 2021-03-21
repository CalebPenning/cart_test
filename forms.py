from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length, InputRequired

class AddItemForm(FlaskForm):
    """form for adding item to cart"""
    quantity = IntegerField('quantity', validators=[DataRequired()])
    
    
class NewUserForm(FlaskForm):
    """"Form for adding a new user."""
    
    username = StringField("Username", validators=[InputRequired(message="Please enter your username."), Length(min=1, max=30)])
    
    email = StringField(label="Email Address", validators=[Email(message="Please enter a valid email address.")])
    
    password = PasswordField("Password", validators=[InputRequired(message="Please enter a password.")])
    
    first_name = StringField("First Name", validators=[Length(min=0, max=40)])
    
    last_name = StringField("Last Name", validators=[Length(min=0, max=40)])
    
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message="Please enter your username.")])
    
    password = PasswordField("Password", validators=[InputRequired(message="Please enter your password.")])