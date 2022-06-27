import email
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):
    """User Registration Form"""

    username = StringField(
        "Username:", validators=[InputRequired(), Length(min=5, max=20)], 
    )
    password = PasswordField(
        "Password:", validators=[InputRequired(),Length(min=5, max=20)], 

    )

    email= StringField(
        "Email:", validators=[InputRequired(), Email(), Length(max=50)],
    )

    first_name = StringField(
        "First Name:", validators=[InputRequired(), Length(max=30)]
    )
    last_name = StringField("Last Name:", validators=[InputRequired(), Length(max=30)])

class LoginForm(FlaskForm):
    """User Login Form"""

    username = StringField(
        "Username:", validators=[InputRequired(),Length(min=5, max=50)], 
    )

    password = PasswordField(
    "Password:", validators=[InputRequired(),Length(min=5, max=20)],)

class FeedbackForm(FlaskForm):
    """Add Feedback Form"""
    title = StringField(
        "Title:", validators=[InputRequired(), Length(max=100)]
    )
    content = StringField(
        "Content:", validators=[InputRequired()]
    )

class DeleteForm(FlaskForm):
    """Delete Form"""

