from Project import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    # profile_image=db.Column(db.BLOB)
    email=db.Column(db.String(64), unique=True, index=True)
    username=db.Column(db.String(64), unique=True, index=True)
    password_hash=db.Column(db.String(128))

    investment_pref1=db.Column(db.String)
    investment_pref2=db.Column(db.String)

    deposit_pref=db.Column(db.String)

    current_assets=db.Column(db.Float)

    expenditure=db.relationship('Expenditures', backref='investor', lazy=True)
    incomes=db.relationship('Incomes', backref='investor', lazy=True)
    # donations=db.relationship('Donations', backref='investor', lazy=True)


    def __init__(self, email, username, password, ip1, ip2, deposit_pref, current_assets):
        self.email=email
        self.username=username
        self.password_hash=generate_password_hash(password)
        self.investment_pref1=ip1
        self.investment_pref2=ip2
        self.deposit_pref=deposit_pref
        self.current_assets=current_assets
    
    def check_password(self, password):
        return check_password_hash(self.password_hash,password)
    
    def __repr__(self):
        return f"Username {self.username}"

# class Investments(db.Model):
#     # __tablename__='investments'
#     users=db.relationship(User)

#     id=db.Column(db.Integer, primary_key=True)
#     user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     date=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     investment_type=db.Column(db.String)
#     investment_name=db.Column(db.String)
#     investment_amount=db.Column(db.Float)

#     def __init__(self, investment_type, investment_name, user_id, investment_amount,d):
#         self.investment_name=investment_name
#         self.investment_type=investment_type
#         self.user_id=user_id
#         self.investment_amount=investment_amount
#         self.date=d
    
#     def __repr__(self):
#         return f"Investment ID: {self.id} --- Date: {self.date} --- {self.investment_name}"

# class Donations(db.Model):
#     users=db.relationship(User)

#     id=db.Column(db.Integer, primary_key=True)
#     user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     date=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     donation_type=db.Column(db.String)
#     donation_name=db.Column(db.String)
#     donation_amount=db.Column(db.Float)

#     def __init__(self, donation_type, donation_name, user_id,d,amount):
#         self.donation_name=donation_name
#         self.donation_type=donation_type
#         self.user_id=user_id
#         self.date=d
#         self.donation_amount=amount
    
#     def __repr__(self):
#         return f"Donation ID: {self.id} --- Date: {self.date} --- {self.donation_name}"

class Expenditures(db.Model):
    users=db.relationship(User)

    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date=db.Column(db.Date, nullable=False, default=datetime.utcnow)
    expenditure_type=db.Column(db.String)
    payee=db.Column(db.String)
    expenditure_amount=db.Column(db.Float)

    def __init__(self, expenditure_type,user_id,d,payee, amount):
        # self.expenditure_name=expenditure_name
        self.expenditure_type=expenditure_type
        self.user_id=user_id
        self.date=d
        self.payee=payee
        self.expenditure_amount=amount
    
    def __repr__(self):
        return f"Expenditure ID: {self.id} --- Date: {self.date} --- {self.expenditure_type}"

class InvestmentsList(db.Model):
    
    id=db.Column(db.Integer, nullable=False, primary_key=True)
    # date=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    listing_name=db.Column(db.String)
    listing_category=db.Column(db.String)
    listing_risk=db.Column(db.String)
    listing_1yreturns=db.Column(db.String)
    listing_rating=db.Column(db.String)
    listing_fund_size=db.Column(db.String)
    listing_link=db.Column(db.String)
    listing_fund_type=db.Column(db.String)

    def __init__(self, listing_name, listing_category, listing_risk, listing_1yreturns, listing_rating, listing_fund_size, listing_link, listing_fund_type):
        self.listing_name=listing_name
        self.listing_category=listing_category
        self.listing_risk=listing_risk
        self.listing_1yreturns=listing_1yreturns
        self.listing_rating=listing_rating
        self.listing_fund_size=listing_fund_size
        self.listing_link=listing_link
        self.listing_fund_type=listing_fund_type

    
    def __repr__(self):
        return f"Listing ID: {self.id} --- Date: {self.date} --- {self.listing_name} --- Cost: {self.listing_cost}"


class DepositsList(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    Bank=db.Column(db.String)
    Rate_Normal=db.Column(db.String)
    Rate_Senior=db.Column(db.String)
    Link=db.Column(db.String)
    Deposit_Type=db.Column(db.String)

    def __init__(self, Bank, Rate_Normal, Rate_Senior, Link, Deposit_Type):
        self.Bank=Bank
        self.Rate_Normal=Rate_Normal
        self.Rate_Senior=Rate_Senior
        self.Link=Link
        self.Deposit_Type=Deposit_Type
    
    def __repr__(self):
        return f"Listing ID: {self.id} --- Bank: {self.Bank} --- Deposit Type: {self.Deposit_Type}"

class Incomes(db.Model):
    # __tablename__='investments'
    users=db.relationship(User)

    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date=db.Column(db.Date, nullable=False, default=datetime.utcnow)
    income_source=db.Column(db.String)
    source_name=db.Column(db.String)
    income_amount=db.Column(db.Float)

    def __init__(self, user_id, date, income_source, source_name, income_amount):
        self.user_id=user_id
        self.date=date
        self.income_source=income_source
        self.source_name=source_name
        self.income_amount=income_amount
    
    def __repr__(self):
        return f"Income ID: {self.id} --- Date: {self.date} --- {self.income_name}"

