from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,SelectField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField



class RegisterUser(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    last_name = StringField("UserName",validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Sign Me Up")


class LoginUser(FlaskForm):
    email = StringField("Email",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Log In")
