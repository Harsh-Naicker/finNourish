from flask import Flask, flash, render_template, request, Blueprint, redirect, url_for
from Project.core.forms import RegistrationForm, LoginForm, ContactForm, UpdateListing, IncomeForm, ExpenditureForm
from Project.models import User, InvestmentsList, DepositsList, Incomes, Expenditures
from Project import db, mail
from flask_login import login_user, current_user, logout_user, login_required
import time
import requests
import lxml.html as lh
import pandas as pd
import re
import sqlite3 as sql
from sqlite3 import Error
from sqlalchemy import create_engine
from flask_mail import Mail, Message
import psycopg2

core=Blueprint('core',__name__)

DATABASE_URL='postgres://cmreepqbqbovqd:fd3fc3ff00a90486bfbba4ce5742a70f6f953d3b3f516d0c672577a8490e5763@ec2-54-196-89-124.compute-1.amazonaws.com:5432/d62ikdp30jv2bj'
engine=create_engine("postgres://cmreepqbqbovqd:fd3fc3ff00a90486bfbba4ce5742a70f6f953d3b3f516d0c672577a8490e5763@ec2-54-196-89-124.compute-1.amazonaws.com:5432/d62ikdp30jv2bj")

def signup_mail(name,email):
    global mail
    msg=Message('Welcome to finNourish!',recipients=[email])
    msg.html='''<div class="body_changes" style="color: white; background-color: #000000; background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: cover; width:750px; margin-right: auto; margin-left: auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;" >

        <div style="margin-right: 20px;margin-left: 20px;">
            <br>
            <img src="https://i.ibb.co/2qG2YCw/fin-Nourish.png%22" style="width:400px;display: block; margin-left: auto; margin-right: auto;" align="center;" alt="finNourish-Logo" border="0">
            
            <p style="font-size: 130%;color: #14bf98;">
                <b>Dear {},</b>
            </p>
            <p style="font-size: 130%;text-align: justify;color: white;">
                Thank you for signing up with <span style="color: #14bf98"><b>finNourish!</b></span> To avail our dedicated <span style="color: #14bf98"><b>smart investments and deposits recommendations</b></span> log into your account and experience seemless access to the latest information.
                <br><br>
                Track your income and expenses with our <span style="color: #14bf98"><b>budget tracker</b></span>. You can monitor your assets, sources of income, categories of expenditures and monthly savings.
            </p>
            <p style="font-size: 130%;color: #14bf98;">
                <b>
                    Regards,<br>
                    Team finNourish
                </b>

            </p>
            
            <p>
                <a href="https://fin-nourish.herokuapp.com/" target="_blank"><button type="button" style="  border: none;
                    color: white;
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 15px;
                   
                    cursor: pointer;
                    background-color: #14bf98;"><b>Visit Website</b></button></a>
    
            </p>

            
            <br>

            
        

        </div>

    </div>'''.format(name)
    
    mail.send(msg)

def contact_mail(name,email, message):
    global mail
    msg=Message('Thank you for contacting us!',recipients=[email])
    msg.html='''<div class="body_changes" style="color: white; background-color: #000000; background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: cover; width:750px; margin-right: auto; margin-left: auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;" >

        <div style="margin-right: 20px;margin-left: 20px;">
            <br>
            <img src="https://i.ibb.co/2qG2YCw/fin-Nourish.png%22" style="width:400px;display: block; margin-left: auto; margin-right: auto;" align="center;" alt="finNourish-Logo" border="0">
            
            <p style="font-size: 130%;color: #14bf98;">
                <b>Dear {},</b>
            </p>
            <p style="font-size: 130%;text-align: justify;color: white;">
                Thank you for reaching out to <span style="color: #14bf98"><b>finNourish!</b></span> Somebody from our team will contact you soon to better serve you and address your query.
                
            </p>
            <p style="font-size: 130%;color: #14bf98;">
                <b>
                    Regards,<br>
                    Team finNourish
                </b>

            </p>
            
            <p>
                <a href="https://fin-nourish.herokuapp.com/" target="_blank"><button type="button" style="  border: none;
                    color: white;
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 15px;
                   
                    cursor: pointer;
                    background-color: #14bf98;"><b>Visit Website</b></button></a>
    
            </p>

            
            <br>

            
        

        </div>

    </div>'''.format(name)
    
    mail.send(msg)
    msg2=Message('New Contact Enquiry',recipients=['finnourish@gmail.com'])
    msg2.body='Name of Applicant: {}\n\nEmail ID: {}\n\nMessage: {}'.format(name,email,message)
    mail.send(msg2)


# def admin_mail(name, email, message):
#     global mail
    
#     msg2=Message('New Contact Enquiry',recipients=['finnourish@gmail.com'])
#     msg2.body='Name of Applicant: {}\n\nEmail ID: {}\n\nMessage: {}'.format(name,email,message)
#     mail.send(msg2)

def get_recurring_deposits(url):
    page = requests.get(url)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//tr')
    col = []
    i = 0

    for t in tr_elements[6]:
        i+=1
        name = t.text_content()
        col.append((name,[]))
    
    for j in range(7,len(tr_elements)):
        T = tr_elements[j]
        if len(T)!=3:
            break
        i = 0
        for t in T.iterchildren():
            data = t.text_content()
            if i>0:
                try:
                    data = int(data)
                except:
                    pass
            col[i][1].append(data)
            i+=1
        
    Dict = {title:column for (title,column) in col}
    df = pd.DataFrame(Dict)
    link = doc.xpath('//tr/td/a[@href]/@href')
    link = list(dict.fromkeys(link))
    link = link[0:19]
    df['Link'] = link
    df['Deposit Type'] = 'Recurring Deposits'

    return df

def get_fixed_deposits(url):
    page = requests.get(url)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//tr')
    col = []
    i = 0

    for t in tr_elements[6]:
        i+=1
        name = t.text_content()
        col.append((name,[]))

    for j in range(7,len(tr_elements)):
        T = tr_elements[j]
        if len(T)!=3:
            break
        i = 0
        for t in T.iterchildren():
            data = t.text_content()
            if i>0:
                try:
                    data = int(data)
                except:
                    pass
            col[i][1].append(data)
            i+=1

    Dict = {title:column for (title,column) in col}
    df = pd.DataFrame(Dict)
    df = df.replace('\r',"",regex=True)
    df = df.replace('\n',"",regex=True)
    heading = []
    for head in df.columns.tolist():
        data = re.sub('\n',"",head)
        data = re.sub('\r',"",data)
        heading.append(data)
    df.columns = heading
    df = df[0:15]
    link = doc.xpath('//tr/td/p/span/a[@href]/@href')
    link.insert(9,'https://www.myloancare.in/fixed-deposit/fd-interest-rates/obc')
    link.insert(13,'https://groww.in/p/fixed-deposit/indian-overseas-bank-fd-interest-rates/')
    link.insert(14,'https://www.myloancare.in/fixed-deposit/fd-interest-rates/pnb-housing-finance')
    df['Link'] = link
    df['Deposit Type'] = 'Fixed Deposits'
    return df

def get_deposits():
    rd_url = 'https://cleartax.in/s/rd-interest-rates'
    fd_url = 'https://cleartax.in/s/fixed-deposits'
    df1=get_recurring_deposits(rd_url)
    df2=get_fixed_deposits(fd_url)
    df2=df2.rename(columns={"Bank List": "Bank", "For Regular Customers (% p.a.)": "Normal Citizens","For Senior Citizens (% p.a.)": "Senior Citizens"})
    df = pd.concat([df1, df2])
    return df

def get_fund_details(url,investment):
    page = requests.get(url)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//tr')
    col = []
    i = 0

    for t in tr_elements[0]:
        i+=1
        name = t.text_content()
        col.append((name,[]))
    for j in range(1,len(tr_elements)):
        T = tr_elements[j]
        if len(T)!=7:
            break
        i = 0
        for t in T.iterchildren():
            data = t.text_content()
            if i>0:
                try:
                    data = int(data)
                except:
                    pass
            col[i][1].append(data)
            i+=1
    Dict = {title:column for (title,column) in col}
    df = pd.DataFrame(Dict)
    df = df.drop(axis=0,index=15)
    link = doc.xpath('//tr/td/a[@href]/@href')
    link = link[0:len(df)]
    link = ['https://groww.in'+ x for x in link]
    df['Link'] = link
    df['Fund Type'] = investment
    
    return df

def mutual_funds_scraper():
    URL_Dict = {
            'Equity_Mutual_Funds':'https://groww.in/mutual-funds/category/best-equity-mutual-funds',
            'Liquid_Mutual_Funds':'https://groww.in/mutual-funds/category/best-liquid-mutual-funds',
            'Short_term_Mutual_Funds':'https://groww.in/mutual-funds/category/best-ultra-short-mutual-funds',
            'Arbitrage_Mutual_Funds':'https://groww.in/mutual-funds/category/best-arbitrage-mutual-funds',
            'Debt_Mutual_Funds':'https://groww.in/mutual-funds/category/best-debt-mutual-funds',
            'Dynamic_Mutual_Funds':'https://groww.in/mutual-funds/category/best-dynamic-mutual-funds'}
    df1 = pd.DataFrame()
    for url in URL_Dict:
        investment = url
        df1 = df1.append(get_fund_details(URL_Dict[url],investment),ignore_index=True)
    
    return df1

def connect_to_db(db_file):
    sql_conn = None
    try:
        sql_conn = psycopg2.connect(db_file, sslmode='require')
        return sql_conn
    except Error as err:
        print(err)
        
        if sql_conn is not None:
            sql_conn.close()

def insert_value_to_deposits_table(table_name,data_frame):
    global engine
    conn = connect_to_db(DATABASE_URL)
    # engine=create_engine("postgres://cmreepqbqbovqd:fd3fc3ff00a90486bfbba4ce5742a70f6f953d3b3f516d0c672577a8490e5763@ec2-54-196-89-124.compute-1.amazonaws.com:5432/d62ikdp30jv2bj")
    # conn=engine.connect()
    if conn is not None:
        c = conn.cursor()
        # c.execute('CREATE TABLE IF NOT EXISTS '+table_name+
        #           '(id                  INTEGER,'
        #           'Bank                 VARCHAR,'
        #           'Rate_Normal          VARCHAR,'
        #           'Rate_Senior          VARCHAR,'
        #           'Link                 VARCHAR,'
        #           'Deposit_Type         VARCHAR)')
        df = data_frame
        df.insert(0,'ID',df.index+1)
        # df = df.drop('',axis = 1)
        df.columns = get_column_names_from_db_table(c,table_name)
        df.to_sql(table_name,con=engine.connect(),if_exists='replace',index=False)
        conn.commit()
        conn.close()
        print('SQL insert process finished')
    else:
        print('Connection to database failed')

def insert_value_to_table(table_name,data_frame):
    global engine
    conn = connect_to_db(DATABASE_URL)
    # engine=create_engine("postgres://cmreepqbqbovqd:fd3fc3ff00a90486bfbba4ce5742a70f6f953d3b3f516d0c672577a8490e5763@ec2-54-196-89-124.compute-1.amazonaws.com:5432/d62ikdp30jv2bj")
    # conn=engine.connect()
    if conn is not None:
        c = conn.cursor()
    #     c.execute('CREATE TABLE IF NOT EXISTS '+table_name+
    #               '(id                  INTEGER,'
    #               'listing_name         VARCHAR,'
    #               'listing_category     VARCHAR,'
    #               'listing_risk         VARCHAR,'
    #               'listing_1yreturns    VARCHAR,'
    #               'listing_rating       VARCHAR,'
    #               'listing_fund_size    VARCHAR,'
    #               'listing_link         VARCHAR,'
    #               'listing_fund_type    VARCHAR)')
        df = data_frame
        df.insert(0,'ID',df.index+1)
        df = df.drop('',axis = 1)
        df.columns = get_column_names_from_db_table(c,table_name)
        df.to_sql(table_name,con=engine.connect(),if_exists='replace',index=False)
        conn.commit()
        conn.close()
        print('SQL insert process finished')
    else:
        print('Connection to database failed')

def get_column_names_from_db_table(sql_cursor,table_name):
    # table_column_names = "PRAGMA table_info("+table_name+");"
    table_column_names= "SELECT COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '"+table_name+"'"
    sql_cursor.execute(table_column_names)
    table_column_names = sql_cursor.fetchall()
    
    column_names = list()
    for name in table_column_names:
        column_names.append(name[0])
    return column_names



@core.route('/',methods=['GET','POST'])
def index():
    form2=RegistrationForm()
    form1=LoginForm()
    form4=ContactForm()
    # form5=UpdateListing()
    form6=IncomeForm()
    form7=ExpenditureForm()

    if form2.submit2.data and form2.validate():
        if User.query.filter_by(email=form1.email.data).first() == None:
            user=User(email=form2.email.data, username=form2.username.data, password=form2.password.data, ip1=form2.invpref1.data, ip2=form2.invpref2.data, deposit_pref=form2.depopref.data, current_assets=form2.current_balance.data)
            signup_mail(form2.username.data, form2.email.data)
            db.session.add(user)
            db.session.commit()
        else:
            flash('An account with this username already exists')
            time.sleep(3)

        
        return redirect(url_for('core.index'))
    
    if form1.submit1.data and form1.validate():

        user=User.query.filter_by(email=form1.email.data).first()
        if user is not None and user.check_password(form1.password.data):
            login_user(user)
            flash('Log in Success')
            next=request.args.get('next')

            # final = mutual_funds_scraper()
            # insert_value_to_table('investments_list',final)

            # deposits=get_deposits()
            # deposits.index=[i for i in range(len(deposits.index))]
            # insert_value_to_deposits_table('deposits_list',deposits)

            if next==None or not next[0]=='/':
                next=url_for('core.index')

            return redirect(next)
    
    if form4.submit4.data and form4.validate():
        contact_mail(form4.name.data, form4.email.data, form4.message.data)
        # admin_mail(form4.name.data, form4.email.data, form4.message.data)
        return redirect(url_for('core.index'))
    
    # if form5.submit5.data and form5.validate():
        
    #     final = mutual_funds_scraper()
    #     insert_value_to_table('investments_list',final)

    #     deposits=get_deposits()
    #     deposits.index=[i for i in range(len(deposits.index))]
    #     insert_value_to_deposits_table('deposits_list',deposits)

        
        # db.session.query(DepositsList).delete()
        # db.session.commit()
        # deposits=get_deposits()
        # for i in range(len(deposits.index)):
        #     deposit=DepositsList(Bank=deposits.iloc[i]['Bank'],Rate_Normal=deposits.iloc[i]['Normal Citizens'], Rate_Senior=deposits.iloc[i]['Senior Citizens'], Link=deposits.iloc[i]['Link'], Deposit_Type=deposits.iloc[i]['Deposit Type'])
        #     db.session.add(deposit)
        #     db.session.commit()

        # return redirect(url_for('core.index'))
    
    if form6.submit6.data and form6.validate():
        income=Incomes(user_id=current_user.id, date=form6.date.data, income_source=form6.source.data, source_name=form6.name.data, income_amount=form6.amount.data)
        current_user.current_assets+=form6.amount.data
        db.session.add(income)
        db.session.commit()
        form6.date.data=None
        form6.source.data=None
        form6.name.data=None
        form6.amount.data=None
        return redirect(url_for('core.index'))
    
    if form7.submit7.data and form7.validate():
        expense=Expenditures(expenditure_type=form7.category.data, user_id=current_user.id, d=form7.date.data, payee=form7.name.data, amount=form7.amount.data)
        current_user.current_assets-=form7.amount.data
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('core.index'))

    
    investments=None
    investments2=None
    deposits=None
    if(current_user.is_authenticated):
        investments=InvestmentsList.query.filter_by(listing_fund_type=current_user.investment_pref1).paginate(per_page=100)
        investments2=InvestmentsList.query.filter_by(listing_fund_type=current_user.investment_pref2).paginate(per_page=100)
        deposits=DepositsList.query.filter_by(Deposit_Type=current_user.deposit_pref).paginate(per_page=100)


    return render_template('index.html', form1=form1, form2=form2, form4=form4, form6=form6, form7=form7, investments=investments, investments2=investments2, deposits=deposits)