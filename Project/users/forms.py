from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from Project.models import User

class UpdateUserForm(FlaskForm):
    email= StringField('Email', validators=[DataRequired(), Email()])
    username=StringField('Username', validators=[DataRequired()])

    invpref1=SelectField('Investment Preference 1', choices=[('Equity_Mutual_Funds','Equity Mutual Funds'), ('Liquid_Mutual_Funds','Liquid Mutual Funds'), ('Short_term_Mutual_Funds','Short Term Mutual Funds'),('Arbitrage_Mutual_Funds','Arbitrage Mutual Funds'), ('Debt_Mutual_Funds','Debt Mutual Funds'), ('Dynamic_Mutual_Funds','Dynamic Mutual Funds')])    
    invpref2=SelectField('Investment Preference 2', choices=[('Equity_Mutual_Funds','Equity Mutual Funds'), ('Liquid_Mutual_Funds','Liquid Mutual Funds'), ('Short_term_Mutual_Funds','Short Term Mutual Funds'),('Arbitrage_Mutual_Funds','Arbitrage Mutual Funds'), ('Debt_Mutual_Funds','Debt Mutual Funds'), ('Dynamic_Mutual_Funds','Dynamic Mutual Funds')])
    depopref=SelectField('Deposit Preference', choices=[('Recurring Deposits','Recurring Deposits'), ('Fixed Deposits','Fixed Deposits')])
    # donpref1=RadioField('Donation Preference 1', choices=[('Type 1','Type 1'), ('Type 2','Type 2')])    
    # donpref2=RadioField('Donation Preference 2', choices=[('Type 1','Type 1'), ('Type 2','Type 2')])
    submit=SubmitField('Update')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Your username has been registered already!')

class ChangePassword(FlaskForm):
    password=PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords must match!')])
    pass_confirm=PasswordField('Confirm Password', validators=[DataRequired()])
    submit2=SubmitField('Change Password')