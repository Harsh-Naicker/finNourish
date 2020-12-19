from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from Project import db, mail, app
from Project.models import User
from Project.users.forms import UpdateUserForm, ChangePassword
from Project.core.forms import ContactForm
import time
from flask_mail import Mail, Message
import psycopg2
import datetime

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.figure_factory as ff
import plotly.graph_objs as go
import pandas as pd
import sqlite3 as sql
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc

users = Blueprint('users', __name__)

DATABASE_URL = 'postgres://cmreepqbqbovqd:fd3fc3ff00a90486bfbba4ce5742a70f6f953d3b3f516d0c672577a8490e5763@ec2-54-196-89-124.compute-1.amazonaws.com:5432/d62ikdp30jv2bj'


def contact_mail(name, email, message):
    global mail
    msg = Message('Thank you for contacting us!', recipients=[email])
    msg.html = '''<div class="body_changes" style="color: white; background-color: #000000; background-repeat: no-repeat;
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
    msg2 = Message('New Contact Enquiry', recipients=['finnourish@gmail.com'])
    msg2.body = 'Name of Applicant: {}\n\nEmail ID: {}\n\nMessage: {}'.format(
        name, email, message)
    mail.send(msg2)





def fetch_data(q):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    df = pd.read_sql(sql=q, con=conn)
    conn.close()
    return df


def get_income_source():
    # income_source = (
    #     f'''SELECT DISTINCT income_source FROM incomes WHERE user_id = '''+ str(cur_user)
    # )
    income_sources = ['Salary', 'Dividends',
                      'Rentals', 'Part Time', 'Miscellaneous']
    # income_sources = fetch_data(income_source)
    # income_sources = list(income_sources['income_source'].sort_values(ascending=True))
    income_sources = sorted(income_sources)
    income_options = (
        [{'label': division, 'value': division}
         for division in income_sources]
    )
    return income_options


def get_expenses_type():
    # expense_type = (
    # f'''SELECT DISTINCT expenditure_type FROM expenditures WHERE user_id = '''+ str(cur_user)
    # )
    expense_cat = ['Electronics', 'Grocery', 'Clothing', 'Entertainment',
                   'Medical Expenses', 'Travelling', 'Rent/Housing Bills', 'Miscellaneous']
    expense_cat = sorted(expense_cat)
    # expense_cat = fetch_data(expense_type)
    # expense_cat = list(expense_cat['expenditure_type'].sort_values(ascending=True))
    expense_options = (
        [{'label': division, 'value': division}
         for division in expense_cat]
    )
    return expense_options


def get_income():
    income = f'''SELECT * FROM incomes WHERE user_id = ''' + str(cur_user)
    df = fetch_data(income)
    return df


def get_expenses():
    expenses = f'''SELECT * FROM expenditures WHERE user_id = ''' + \
        str(cur_user)
    df = fetch_data(expenses)
    return df


def pie_chart_income():
    income = get_income()
    income_source = income['income_source']
    income_amount = income['income_amount']
    v = [0, 0, 0]
    l = ['a', 'b', 'c']
    fig = go.Figure(
        data=[go.Pie(labels=l, values=v, name="<b>Income Distribution</b>")])
    fig.update_layout(
        title_text="<b>No Income Data Available</b>",
        annotations=[dict(text='', x=0.50, y=0.5, font_size=20, showarrow=False)], paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )

    if len(income_amount) != 0:
        fig = go.Figure(data=[go.Pie(
            labels=income_source, values=income_amount, name="<b>Income Distribution</b>")])
        fig.update_traces(hole=0.4, hoverinfo="label+percent+name")

        fig.update_layout(
            title_text="<b>Income Distribution</b>",
            annotations=[dict(text='Income', x=0.50, y=0.5, font_size=20, showarrow=False)], paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )

    return fig


def pie_chart_expense():
    expenses = get_expenses()
    expense_cat = expenses['expenditure_type']
    expense_amt = expenses['expenditure_amount']

    v = [0, 0, 0]
    l = ['a', 'b', 'c']
    fig = go.Figure(
        data=[go.Pie(labels=l, values=v, name="<b>Expenditure Distribution</b>")])
    fig.update_layout(
        title_text="<b>No Expense Data Available</b>",
        annotations=[dict(text='', x=0.50, y=0.5, font_size=20, showarrow=False)], paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )

    if len(expense_amt) != 0:
        fig = go.Figure(data=[go.Pie(
            labels=expense_cat, values=expense_amt, name="<b>Expenditure Distribution</b>")])
        fig.update_traces(hole=0.4, hoverinfo="label+percent+name")

        fig.update_layout(
            title_text="<b>Expenditure Distribution</b>",
            annotations=[dict(text='Expense', x=0.50, y=0.5, font_size=20, showarrow=False)], paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )

    return fig


def income_chart(value):
    df = get_income()
    dates = df[df['income_source'] == value]['date']
    amount = df[df['income_source'] == value]['income_amount']
    source = df[df['income_source'] == value]['source_name']
    defx = [1, 2, 3, 4]
    defy = [0, 0, 0, 0]
    figure = go.Figure(
        data=[
            go.Bar(x=defx, y=defy, marker_color='#14bf98')
        ],
        layout=go.Layout(
            title='<b>No Income Data</b>',
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
    )
    if len(dates) != 0:
        figure = go.Figure(
            data=[
                go.Bar(x=dates, y=amount, text=source,
                       textposition='auto', marker_color='#14bf98')
            ],
            layout=go.Layout(
                xaxis={'type': 'category'},
                title='<b>Amount From '+str(value)+'</b>',
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
        )

    return figure


def expenses_chart(value):
    df = get_expenses()
    dates = df[df['expenditure_type'] == value]['date']
    dates = [str(i) for i in dates]
    amount = df[df['expenditure_type'] == value]['expenditure_amount']
    item = df[df['expenditure_type'] == value]['payee']

    defx = [1, 2, 3, 4]
    defy = [0, 0, 0, 0]
    figure = go.Figure(
        data=[
            go.Bar(x=defx, y=defy, marker_color='#14bf98')
        ],
        layout=go.Layout(
            title='<b>No Expense Data</b>',
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
    )

    if len(dates) != 0:
        figure = go.Figure(
            data=[
                go.Bar(x=dates, y=amount, text=item,
                       textposition='auto', marker_color='#14bf98')
            ],
            layout=go.Layout(
                xaxis={'type': 'category'},
                title='<b>Amount used for '+str(value)+'</b>',
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
        )

    # figure.update_xaxes(ticklabelmode="period")
    return figure


def get_saving():
    per_month_income = f'''SELECT to_char(date,'MM-YYYY') AS Month,SUM(income_amount) AS Total_Income FROM incomes WHERE user_id = ''' + str(
        cur_user)+''' GROUP BY 1'''
    df = fetch_data(per_month_income)
    per_month_expenses = f'''SELECT to_char(date,'MM-YYYY') AS Month,SUM(expenditure_amount) AS Total_Expenses FROM expenditures WHERE user_id = ''' + str(
        cur_user)+''' GROUP BY 1'''
    df1 = fetch_data(per_month_expenses)
    result = pd.merge(df1, df, on=['month'], how='outer')
    result = result.fillna(0)
    cur = f'''SELECT current_assets FROM users WHERE id = '''+str(cur_user)
    cur_asset = fetch_data(cur)
    cur_asset = cur_asset.values[0][0]
    result['Savings Per month'] = result['total_income'] - \
        result['total_expenses']
    result['Cumulative Savings'] = result['Savings Per month'].cumsum()
    result['Cumulative Savings'] = result['Cumulative Savings']
    # for i in range(len(result['Expense_Date'])):
    #     if result['Expense_Date'][i]==0:
    #         result['Expense_Date'][i]=result['Income_Date'][i]
    return result


def get_my(i):
    date = datetime.datetime.strptime(i, '%Y-%m-%d')
    Date = date.strftime("%b") + ' ' + date.strftime("%Y")
    return Date

dash_app = dash.Dash(__name__, server=app, url_base_pathname='/tracker/', external_stylesheets=[dbc.themes.MINTY])
dash_app.title='finNourish'
for view_func in app.view_functions:
    if view_func.startswith(dash_app.config['url_base_pathname']):
        app.view_functions[view_func] = login_required(app.view_functions[view_func])

cur_user=0
# if current_user!=None and current_user.is_authenticated:
#     cur_user=current_user.id


dash_app.layout = html.Div([
    dbc.Row([dbc.Col(html.Div(className="logo",children=[
                    html.Img(src='https://i.ibb.co/BC33M3V/JH-Solutions-1.png%22')
                    ]),
                    width = {'size':5},
                   ),
            dbc.Col(html.H1("Budget Tracker"),
                    width = {'size':3,'offset':5},
                   ),
    ]),
    dbc.Row(dbc.Col(html.H4("Select Income Source and Expense Category"),

                   ),
           ),
    dbc.Row(
    [

        dbc.Col(dcc.Dropdown(id='income-selector',
                             placeholder = 'Income Sources',
                             options=get_income_source(),
                             value='Total Income'),
                width={'size':5,'offset':1,'order':1}
               ),
        dbc.Col(dcc.Dropdown(id='expense-selector',
                             placeholder = 'Expense Category',
                             options = get_expenses_type(),
                             value = 'Combined Expenses'),
               width={'size':5,'offest':1,'order':2}
               ),
    ], no_gutters=True
    ),
    dbc.Row(
    [
        dbc.Col(html.Div(className="graph",children=[
            dcc.Graph(id='pie_chart1',figure={})

        ]),width=6,lg={'size':6,'offset':0,'order':'first'}),

        dbc.Col(html.Div(className="graph",children=[
            dcc.Graph(id='pie_chart2',figure={})

        ]),width=6,lg={'size':6,'offset':0,'order':'last'}),
    ]
    ),

    dbc.Row(
    [
        dbc.Col(dcc.Graph(id='savings-chart',figure={}),
               width=6,lg={'size':6,'offset':0,'order':'first'}
               ),
        dbc.Col(dcc.Graph(id='cum-saving',figure={}),
               width=6,lg={'size':6,'offset':0,'order':'last'}
               ),
    ])
])

@dash_app.callback(
    [Output('pie_chart1','figure'),
     Output('pie_chart2','figure')],
    [Input('income-selector','value'),
     Input('expense-selector','value')]
)
def update_graph(income,expense):
    global cur_user
    if current_user.is_authenticated:
        cur_user=current_user.id

        pie_fig1=None
        if income=="Total Income" or income==None:
            pie_fig1=pie_chart_income()
        else:
            pie_fig1=income_chart(income)

        pie_fig2=None
        if expense=="Combined Expenses" or expense==None:
            pie_fig2=pie_chart_expense()
        else:
            pie_fig2=expenses_chart(expense)
        return pie_fig1, pie_fig2
    else:
        return '','',''


@dash_app.callback(
    [Output('savings-chart','figure'),
     Output('cum-saving','figure')],
    [Input('income-selector','value')])
def update_savings(value):
    global cur_user
    if current_user.is_authenticated:
        cur_user=current_user.id
        df = get_saving()
        Date=df['month']
        

        Savings = df['Savings Per month']
        Cum_saving = df['Cumulative Savings']
        figure=None
        defx=[1,2,3,4]
        defy=[0,0,0,0]
        figure = go.Figure(
            data = [
                go.Bar(x=defx,y=defy, marker_color='#14bf98')
            ],
            layout=go.Layout(
                title='<b>No Savings Data</b>',
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
        )

        if len(Savings)!=0:
            figure = go.Figure(
                data = [
                    go.Bar(x=Date,y=Savings,text=int(Savings),textposition='auto', marker_color=' #14bf98')
                ],
                layout=go.Layout(
                    title='<b>Amount Saved Per Month</b>',
                    showlegend=False,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
            )
        figure2 = go.Figure(
            data = [
                go.Bar(x=defx,y=defy,marker_color=' #14bf98')
            ],
            layout=go.Layout(
                title='<b>No Cumulative Savings Data</b>',
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
        )

        if len(Cum_saving)!=0:
            figure2 = go.Figure(
                data = [
                    go.Bar(x=Date,y=Cum_saving,text=int(Cum_saving),textposition='auto',marker_color=' #14bf98')
                ],
                layout=go.Layout(
                    title='<b>Net Savings After Each Month</b>',
                    showlegend=False,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
            )


        return figure,figure2
    else:
        return '',''

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()
    form4 = ContactForm()
    form2 = ChangePassword()
    if form.submit.data and form.validate():
        current_user.username = form.username.data
        current_user.email = form.email.data
        # current_user.password_hash=generate_password_hash(form.password.data)
        current_user.investment_pref1 = form.invpref1.data
        current_user.investment_pref2 = form.invpref2.data
        current_user.deposit_pref = form.depopref.data
        # current_user.donation_pref1=form.donpref1.data
        # current_user.donation_pref2=form.donpref2.data
        db.session.commit()
        flash('User account Updated')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    if form4.submit4.data and form4.validate():
        contact_mail(form4.name.data, form4.email.data, form4.message.data)
        # admin_mail(form4.name.data, form4.email.data, form4.message.data)
        return redirect(url_for('users.account'))

    if form2.submit2.data and form2.validate():
        current_user.password_hash = generate_password_hash(
            form2.password.data)
        db.session.commit()
        return redirect(url_for('users.logout'))

    return render_template('account.html', form=form, form4=form4, form2=form2)


@users.route('/dashboard/')
@login_required
def render_tracker():
    global cur_user
    return redirect('/tracker/')
