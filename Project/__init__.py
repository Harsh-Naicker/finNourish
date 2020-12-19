import os
import dash
from dash.dependencies import Input,Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.figure_factory as ff
import plotly.graph_objs as go
import pandas as pd
import sqlite3 as sql
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import datetime
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
import psycopg2

app=Flask(__name__)

app.config['SECRET_KEY']='mysecret'

DATABASE_URL='postgres://cmreepqbqbovqd:fd3fc3ff00a90486bfbba4ce5742a70f6f953d3b3f516d0c672577a8490e5763@ec2-54-196-89-124.compute-1.amazonaws.com:5432/d62ikdp30jv2bj'
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']=DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
Migrate(app,db)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='users.login'

from Project.core.views import core
from Project.users.views import users

app.register_blueprint(core)
app.register_blueprint(users)

cur_user = 1

def fetch_data(q):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    df = pd.read_sql(sql=q,con = conn)
    conn.close()
    return df

def get_income_source():
    # income_source = (
    #     f'''SELECT DISTINCT income_source FROM incomes WHERE user_id = '''+ str(cur_user)
    # )
    income_sources=['Salary','Dividends','Rentals','Part Time', 'Miscellaneous']
    # income_sources = fetch_data(income_source)
    # income_sources = list(income_sources['income_source'].sort_values(ascending=True))
    income_sources=sorted(income_sources)
    income_options = (
    [{'label':division,'value':division}
     for division in income_sources]
    )
    return income_options

def get_expenses_type():
    # expense_type = (
    # f'''SELECT DISTINCT expenditure_type FROM expenditures WHERE user_id = '''+ str(cur_user)
    # )
    expense_cat=['Electronics','Grocery','Clothing','Entertainment','Medical Expenses','Travelling','Rent/Housing Bills','Miscellaneous']
    expense_cat=sorted(expense_cat)
    # expense_cat = fetch_data(expense_type)
    # expense_cat = list(expense_cat['expenditure_type'].sort_values(ascending=True))
    expense_options = (
    [{'label':division,'value':division}
     for division in expense_cat]
    )
    return expense_options

def get_income():
    income = f'''SELECT * FROM incomes WHERE user_id = '''+ str(cur_user)
    df = fetch_data(income)
    return df

def get_expenses():
    expenses = f'''SELECT * FROM expenditures WHERE user_id = '''+ str(cur_user)
    df = fetch_data(expenses)
    return df

def pie_chart_income():
    income = get_income()
    income_source = income['income_source']
    income_amount = income['income_amount']
    v=[0,0,0]
    l=['a','b','c']
    fig = go.Figure(data = [go.Pie(labels=l, values=v,name = "Income Distribution")])
    fig.update_layout(
    title_text = "No Income Data Available",
    annotations=[dict(text='',x=0.50,y=0.5,font_size=20,showarrow=False)]
    )

    if len(income_amount)!=0:
        fig = go.Figure(data = [go.Pie(labels=income_source, values=income_amount,name = "Income Distribution")])
        fig.update_traces(hole = 0.4, hoverinfo="label+percent+name")

        fig.update_layout(
        title_text = "Income Distribution",
        annotations=[dict(text='Income',x=0.50,y=0.5,font_size=20,showarrow=False)]
        )


    
    return fig

def pie_chart_expense():
    expenses = get_expenses()
    expense_cat = expenses['expenditure_type']
    expense_amt = expenses['expenditure_amount']

    v=[0,0,0]
    l=['a','b','c']
    fig = go.Figure(data = [go.Pie(labels=l, values=v,name = "Income Distribution")])
    fig.update_layout(
    title_text = "No Expense Data Available",
    annotations=[dict(text='',x=0.50,y=0.5,font_size=20,showarrow=False)]
    )

    if len(expense_amt)!=0:
        fig = go.Figure(data = [go.Pie(labels=expense_cat, values=expense_amt,name = "Expenditure Distribution")])
        fig.update_traces(hole = 0.4, hoverinfo="label+percent+name")
 

        fig.update_layout(
        title_text = "Expenditure Distribution",
        annotations=[dict(text='Expense',x=0.50,y=0.5,font_size=20,showarrow=False)]
        )

    
    
    return fig

def income_chart(value):
    df = get_income()
    dates = df[df['income_source']==value]['date']
    amount = df[df['income_source']==value]['income_amount']
    source = df[df['income_source']==value]['source_name']
    defx=[1,2,3,4]
    defy=[0,0,0,0]
    figure = go.Figure(
        data = [
               go.Bar(x=defx,y=defy)
        ],
        layout=go.Layout(
            title='No Income Data',
            showlegend=False
        )
    )
    if len(dates)!=0:
        figure = go.Figure(
            data = [
                go.Bar(x=dates,y=amount,text=source,textposition='auto')
            ],
            layout=go.Layout(
                xaxis={'type':'category'},
                title='Amount From '+str(value),
                showlegend=False
            )
        )
    
    return figure

def expenses_chart(value):
    df = get_expenses()
    dates = df[df['expenditure_type']==value]['date']
    dates = [str(i) for i in dates]
    amount = df[df['expenditure_type']==value]['expenditure_amount']
    item = df[df['expenditure_type']==value]['payee']

    defx=[1,2,3,4]
    defy=[0,0,0,0]
    figure = go.Figure(
        data = [
               go.Bar(x=defx,y=defy)
        ],
        layout=go.Layout(
            title='No Expense Data',
            showlegend=False
        )
    )

    if len(dates)!=0:
        figure = go.Figure(
            data = [
                go.Bar(x=dates,y=amount,text=item,textposition='auto')
            ],
            layout=go.Layout(
                xaxis={'type':'category'},
                title='Amount used for '+str(value),
                showlegend=False
            )
        )

    
    
    # figure.update_xaxes(ticklabelmode="period")
    return figure

def get_saving():
    per_month_income = f'''SELECT to_char(date,'MM-YYYY') AS Month,SUM(income_amount) AS Total_Income FROM incomes WHERE user_id = '''+ str(cur_user)+''' GROUP BY 1'''
    df = fetch_data(per_month_income)
    per_month_expenses = f'''SELECT to_char(date,'MM-YYYY') AS Month,SUM(expenditure_amount) AS Total_Expenses FROM expenditures WHERE user_id = '''+ str(cur_user)+''' GROUP BY 1''' 
    df1 = fetch_data(per_month_expenses)
    result = pd.merge(df1,df,on=['month'],how='outer')
    result = result.fillna(0)
    cur = f'''SELECT current_assets FROM users WHERE id = '''+str(cur_user)
    cur_asset = fetch_data(cur)
    cur_asset = cur_asset.values[0][0]
    result['Savings Per month'] = result['total_income'] - result['total_expenses']
    result['Cumulative Savings'] = result['Savings Per month'].cumsum()
    result['Cumulative Savings'] = result['Cumulative Savings']
    # for i in range(len(result['Expense_Date'])):
    #     if result['Expense_Date'][i]==0:
    #         result['Expense_Date'][i]=result['Income_Date'][i]
    return result

def get_my(i):
    date = datetime.datetime.strptime(i,'%Y-%m-%d')
    Date = date.strftime("%b")+ ' '+ date.strftime("%Y")
    return Date

dash_app = dash.Dash(__name__, server=app, url_base_pathname='/tracker/', external_stylesheets=[dbc.themes.MINTY])

dash_app.layout = html.Div([
    dbc.Row(dbc.Col(html.H3("Budget Tracker"),
                    width = {'size':2,'offset':5},
                   ),
           ),
    dbc.Row(dbc.Col(html.Div("Select Income Source and Expense Category"),
                   width = {'size':7,'offset':5},
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
        dbc.Col(dcc.Graph(id='pie_chart1',figure={}),
               width=6,lg={'size':6,'offset':0,'order':'first'}
               ),
        dbc.Col(dcc.Graph(id='pie_chart2',figure={}),
               width=6,lg={'size':6,'offset':0,'order':'last'}
               ),
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
    # if income == "Total Income" or expense == "Combined Expenses":
    #     pie_fig1 = pie_chart_income()
    #     pie_fig2 = pie_chart_expense()
    #     return pie_fig1,pie_fig2
    # elif income !="Total Income" and expense == "Combined Expenses":
    #     fig1 = income_chart(income)
    #     fig2 = pie_chart_expense()
    #     return fig1,fig2
    # elif income == "Total Income" and expense !="Combined Expenses":
    #     fig1 = pie_chart_income()
    #     fig2 = expenses_chart(expense)
    #     return fig1,fig2
    # elif income !="Total Income" and expense !="Combined Expenses":
    #     fig1 = income_chart(income)
    #     fig2 = expenses_chart(expense)
    #     return fig1,fig2
    # else:
    #     fig1 = pie_chart_income()
    #     fig2 = pie_chart_expense()
    #     return fig1,fig2
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
    


@dash_app.callback(
    [Output('savings-chart','figure'),
     Output('cum-saving','figure')],
    [Input('income-selector','value')])
def update_savings(value):
    df = get_saving()
    Date=df['month']
    # Date=[get_my(i) for i in df['Income_Date']]
    # if len(df['Expense_Date'])!=0:
    #     Date = [get_my(i) for i in df['Expense_Date']]
    
    Savings = df['Savings Per month']
    Cum_saving = df['Cumulative Savings']
    figure=None
    defx=[1,2,3,4]
    defy=[0,0,0,0]
    figure = go.Figure(
        data = [
               go.Bar(x=defx,y=defy)
        ],
        layout=go.Layout(
            title='No Savings Data',
            showlegend=False
        )
    )
    
    if len(Savings)!=0:
        figure = go.Figure(
            data = [
                go.Bar(x=Date,y=Savings,text=int(Savings),textposition='auto')
            ],
            layout=go.Layout(
                title='Amount Saved per month ',
                showlegend=False
            )
        )
    figure2 = go.Figure(
        data = [
               go.Bar(x=defx,y=defy)
        ],
        layout=go.Layout(
            title='No Cumulative Savings Data',
            showlegend=False
        )
    )

    if len(Cum_saving)!=0:
        figure2 = go.Figure(
            data = [
                go.Bar(x=Date,y=Cum_saving,text=int(Cum_saving),textposition='auto')
            ],
            layout=go.Layout(
                title='Net Savings After Each Month',
                showlegend=False
            )
        )

    
    
    return figure,figure2

@app.route('/dashboard/<id>')
def render_tracker(id):
    global cur_user
    cur_user=id
    return redirect('/tracker/')