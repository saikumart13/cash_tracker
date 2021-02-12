from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from app.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('User Name', 
                            validators=[Length(min=3, max=15),DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                        validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken, choose another name')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Account exists for this email, choose different one')

class LoginForm(FlaskForm):
    username = StringField('User Name', 
                            validators=[DataRequired(),Length(min=3, max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AddTransactionForm(FlaskForm):
    particulars = StringField('Details',validators=[DataRequired()])
    t_type = RadioField('Transaction Type',choices=['Debit','Credit'], validators=[DataRequired()]) 
    date = DateField('Date',format='%d/%m/%Y')
    amount = IntegerField('Amount',validators=[DataRequired(),NumberRange(min=0)])
    submit = SubmitField('Add Transaction')


class UpdateAccountForm(FlaskForm):
    username = StringField('User Name', 
                            validators=[Length(min=3, max=15),DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(),Email()])
    picture = FileField('Update profile picture',validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already taken, choose another name')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Account exists for this email, choose different one')



