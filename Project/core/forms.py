from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, FloatField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from Project.models import User

class LoginForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password', validators=[DataRequired()])
    submit1=SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email= StringField('Email', validators=[DataRequired(), Email()])
    username=StringField('Username', validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords must match!')])
    pass_confirm=PasswordField('Confirm Password', validators=[DataRequired()])

    invpref1=SelectField('Investment Preference 1', choices=[('Equity_Mutual_Funds','Equity Mutual Funds'), ('Liquid_Mutual_Funds','Liquid Mutual Funds'), ('Short_term_Mutual_Funds','Short Term Mutual Funds'),('Arbitrage_Mutual_Funds','Arbitrage Mutual Funds'), ('Debt_Mutual_Funds','Debt Mutual Funds'), ('Dynamic_Mutual_Funds','Dynamic Mutual Funds')])    
    invpref2=SelectField('Investment Preference 2', choices=[('Equity_Mutual_Funds','Equity Mutual Funds'), ('Liquid_Mutual_Funds','Liquid Mutual Funds'), ('Short_term_Mutual_Funds','Short Term Mutual Funds'),('Arbitrage_Mutual_Funds','Arbitrage Mutual Funds'), ('Debt_Mutual_Funds','Debt Mutual Funds'), ('Dynamic_Mutual_Funds','Dynamic Mutual Funds')])
    depopref=SelectField('Deposit Preference', choices=[('Recurring Deposits','Recurring Deposits'), ('Fixed Deposits','Fixed Deposits')])

    current_balance=FloatField('Current Balance (₹)', validators=[DataRequired()])
    submit2=SubmitField('Sign Up')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has been registered already!")
    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Your username has been registered already!")

class ContactForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    name=StringField('Name', validators=[DataRequired()])
    message=StringField('Message', validators=[DataRequired()])
    submit4=SubmitField('Send Message')

class UpdateListing(FlaskForm):
    submit5=SubmitField('Update Listings')

class IncomeForm(FlaskForm):
    date=DateField('Date (dd-mm-yyyy)', format='%d-%m-%Y', validators=[DataRequired()])
    source=SelectField('Income Source', choices=[('Salary','Salary'),('Dividends','Dividends'),('Rentals','Rentals'),('Part Time','Part Time'),('Miscellaneous','Miscellaneous')], validators=[DataRequired()])
    name=StringField('Source Name', validators=[DataRequired()])
    amount=FloatField('Income Amount', validators=[DataRequired()])
    submit6=SubmitField('Update Incomes')

class ExpenditureForm(FlaskForm):
    date=DateField('Date (dd-mm-yyyy)', format='%d-%m-%Y', validators=[DataRequired()])
    category=SelectField('Expense Category', choices=[('Electronics','Electronics'),('Grocery','Grocery'),('Clothing','Clothing'),('Entertainment','Entertainment'),('Medical Expenses','Medical Expenses'),('Travelling','Travelling'),('Rent/Housing Bills','Rent/Housing Bills'),('Miscellaneous','Miscellaneous')], validators=[DataRequired()])
    name=StringField('Payee', validators=[DataRequired()])
    amount=FloatField('Expense Amount', validators=[DataRequired()])
    submit7=SubmitField('Update Expenses')

# class BudgetTracker(FlaskForm):
#     submit6=SubmitField('Budget Tracker')