import os
# import dash
# from dash.dependencies import Input,Output
# import dash_core_components as dcc
# import dash_html_components as html
# import plotly.figure_factory as ff
# import plotly.graph_objs as go
# import pandas as pd
# import sqlite3 as sql
# from plotly.subplots import make_subplots
# import dash_bootstrap_components as dbc
import datetime
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_required
from flask_mail import Mail, Message
import psycopg2

app=Flask(__name__)

app.config['SECRET_KEY']='mysecret'

# DATABASE_URL='postgres://cmreepqbqbovqd:fd3fc3ff00a90486bfbba4ce5742a70f6f953d3b3f516d0c672577a8490e5763@ec2-54-196-89-124.compute-1.amazonaws.com:5432/d62ikdp30jv2bj'
DATABASE_URL='postgres://wrdnwasvsmdeqy:124ec789f3b8a3ea30f00638b2619fbc167e205b1d99c1d616e00502b3ad30e2@ec2-54-167-168-52.compute-1.amazonaws.com:5432/d6n4hthuhlvp5d'
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']=DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']='finnourish@gmail.com'
app.config['MAIL_PASSWORD']='xqvbkpmmufasomhq'
app.config['MAIL_DEFAULT_SENDER']='finnourish@gmail.com'
app.config['MAIL_MAX_MAILS']=None
app.config['MAIL_ASCII_ATTACHMENTS']=False

mail=Mail(app)

db = SQLAlchemy(app)
Migrate(app,db)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='users.login'

from Project.core.views import core
from Project.users.views import users

app.register_blueprint(core)
app.register_blueprint(users)

# cur_user = 1

# def fetch_data(q):
#     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#     df = pd.read_sql(sql=q,con = conn)
#     conn.close()
#     return df

# def get_income_source():
#     # income_source = (
#     #     f'''SELECT DISTINCT income_source FROM incomes WHERE user_id = '''+ str(cur_user)
#     # )
#     income_sources=['Salary','Dividends','Rentals','Part Time', 'Miscellaneous']
#     # income_sources = fetch_data(income_source)
#     # income_sources = list(income_sources['income_source'].sort_values(ascending=True))
#     income_sources=sorted(income_sources)
#     income_options = (
#     [{'label':division,'value':division}
#      for division in income_sources]
#     )
#     return income_options

# def get_expenses_type():
#     # expense_type = (
#     # f'''SELECT DISTINCT expenditure_type FROM expenditures WHERE user_id = '''+ str(cur_user)
#     # )
#     expense_cat=['Electronics','Grocery','Clothing','Entertainment','Medical Expenses','Travelling','Rent/Housing Bills','Miscellaneous']
#     expense_cat=sorted(expense_cat)
#     # expense_cat = fetch_data(expense_type)
#     # expense_cat = list(expense_cat['expenditure_type'].sort_values(ascending=True))
#     expense_options = (
#     [{'label':division,'value':division}
#      for division in expense_cat]
#     )
#     return expense_options

# def get_income():
#     income = f'''SELECT * FROM incomes WHERE user_id = '''+ str(cur_user)
#     df = fetch_data(income)
#     return df

# def get_expenses():
#     expenses = f'''SELECT * FROM expenditures WHERE user_id = '''+ str(cur_user)
#     df = fetch_data(expenses)
#     return df

# def pie_chart_income():
#     income = get_income()
#     income_source = income['income_source']
#     income_amount = income['income_amount']
#     v=[0,0,0]
#     l=['a','b','c']
#     fig = go.Figure(data = [go.Pie(labels=l, values=v,name = "<b>Income Distribution</b>")])
#     fig.update_layout(
#     title_text = "<b>No Income Data Available</b>",
#     annotations=[dict(text='',x=0.50,y=0.5,font_size=20,showarrow=False)],paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)'
#     )

#     if len(income_amount)!=0:
#         fig = go.Figure(data = [go.Pie(labels=income_source, values=income_amount,name = "<b>Income Distribution</b>")])
#         fig.update_traces(hole = 0.4, hoverinfo="label+percent+name")

#         fig.update_layout(
#         title_text = "<b>Income Distribution</b>",
#         annotations=[dict(text='Income',x=0.50,y=0.5,font_size=20,showarrow=False)],paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)'
#         )


    
#     return fig

# def pie_chart_expense():
#     expenses = get_expenses()
#     expense_cat = expenses['expenditure_type']
#     expense_amt = expenses['expenditure_amount']

#     v=[0,0,0]
#     l=['a','b','c']
#     fig = go.Figure(data = [go.Pie(labels=l, values=v,name = "<b>Expenditure Distribution</b>")])
#     fig.update_layout(
#     title_text = "<b>No Expense Data Available</b>",
#     annotations=[dict(text='',x=0.50,y=0.5,font_size=20,showarrow=False)],paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)'
#     )

#     if len(expense_amt)!=0:
#         fig = go.Figure(data = [go.Pie(labels=expense_cat, values=expense_amt,name = "<b>Expenditure Distribution</b>")])
#         fig.update_traces(hole = 0.4, hoverinfo="label+percent+name")
 

#         fig.update_layout(
#         title_text = "<b>Expenditure Distribution</b>",
#         annotations=[dict(text='Expense',x=0.50,y=0.5,font_size=20,showarrow=False)],paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)'
#         )

    
    
#     return fig

# def income_chart(value):
#     df = get_income()
#     dates = df[df['income_source']==value]['date']
#     amount = df[df['income_source']==value]['income_amount']
#     source = df[df['income_source']==value]['source_name']
#     defx=[1,2,3,4]
#     defy=[0,0,0,0]
#     figure = go.Figure(
#         data = [
#                go.Bar(x=defx,y=defy,marker_color='#14bf98')
#         ],
#         layout=go.Layout(
#             title='<b>No Income Data</b>',
#             showlegend=False,
#             paper_bgcolor='rgba(0,0,0,0)',
#             plot_bgcolor='rgba(0,0,0,0)'
#         )
#     )
#     if len(dates)!=0:
#         figure = go.Figure(
#             data = [
#                 go.Bar(x=dates,y=amount,text=source,textposition='auto',marker_color='#14bf98')
#             ],
#             layout=go.Layout(
#                 xaxis={'type':'category'},
#                 title='<b>Amount From '+str(value)+'</b>',
#                 showlegend=False,
#                 paper_bgcolor='rgba(0,0,0,0)',
#                 plot_bgcolor='rgba(0,0,0,0)'
#             )
#         )
    
#     return figure

# def expenses_chart(value):
#     df = get_expenses()
#     dates = df[df['expenditure_type']==value]['date']
#     dates = [str(i) for i in dates]
#     amount = df[df['expenditure_type']==value]['expenditure_amount']
#     item = df[df['expenditure_type']==value]['payee']

#     defx=[1,2,3,4]
#     defy=[0,0,0,0]
#     figure = go.Figure(
#         data = [
#                go.Bar(x=defx,y=defy,marker_color='#14bf98')
#         ],
#         layout=go.Layout(
#             title='<b>No Expense Data</b>',
#             showlegend=False,
#             paper_bgcolor='rgba(0,0,0,0)',
#             plot_bgcolor='rgba(0,0,0,0)'
#         )
#     )

#     if len(dates)!=0:
#         figure = go.Figure(
#             data = [
#                 go.Bar(x=dates,y=amount,text=item,textposition='auto',marker_color='#14bf98')
#             ],
#             layout=go.Layout(
#                 xaxis={'type':'category'},
#                 title='<b>Amount used for '+str(value)+'</b>',
#                 showlegend=False,
#                 paper_bgcolor='rgba(0,0,0,0)',
#                 plot_bgcolor='rgba(0,0,0,0)'
#             )
#         )

    
    
#     # figure.update_xaxes(ticklabelmode="period")
#     return figure

# def get_saving():
#     per_month_income = f'''SELECT to_char(date,'MM-YYYY') AS Month,SUM(income_amount) AS Total_Income FROM incomes WHERE user_id = '''+ str(cur_user)+''' GROUP BY 1'''
#     df = fetch_data(per_month_income)
#     per_month_expenses = f'''SELECT to_char(date,'MM-YYYY') AS Month,SUM(expenditure_amount) AS Total_Expenses FROM expenditures WHERE user_id = '''+ str(cur_user)+''' GROUP BY 1''' 
#     df1 = fetch_data(per_month_expenses)
#     result = pd.merge(df1,df,on=['month'],how='outer')
#     result = result.fillna(0)
#     cur = f'''SELECT current_assets FROM users WHERE id = '''+str(cur_user)
#     cur_asset = fetch_data(cur)
#     cur_asset = cur_asset.values[0][0]
#     result['Savings Per month'] = result['total_income'] - result['total_expenses']
#     result['Cumulative Savings'] = result['Savings Per month'].cumsum()
#     result['Cumulative Savings'] = result['Cumulative Savings']
#     # for i in range(len(result['Expense_Date'])):
#     #     if result['Expense_Date'][i]==0:
#     #         result['Expense_Date'][i]=result['Income_Date'][i]
#     return result

# def get_my(i):
#     date = datetime.datetime.strptime(i,'%Y-%m-%d')
#     Date = date.strftime("%b")+ ' '+ date.strftime("%Y")
#     return Date

# dash_app = dash.Dash(__name__, server=app, url_base_pathname='/tracker/', external_stylesheets=[dbc.themes.MINTY])
# dash_app.title='finNourish'
# for view_func in app.view_functions:
#     if view_func.startswith(dash_app.config['url_base_pathname']):
#         app.view_functions[view_func] = login_required(app.view_functions[view_func])

# dash_app.layout = html.Div([
#     dbc.Row([dbc.Col(html.Div(className="logo",children=[
#                     html.Img(src='https://i.ibb.co/BC33M3V/JH-Solutions-1.png%22')
#                     ]),
#                     width = {'size':5},
#                    ),
#             dbc.Col(html.H1("Budget Tracker"),
#                     width = {'size':3,'offset':5},
#                    ),
#     ]),
#     dbc.Row(dbc.Col(html.H4("Select Income Source and Expense Category"),
                   
#                    ),
#            ),
#     dbc.Row(
#     [
        
#         dbc.Col(dcc.Dropdown(id='income-selector',
#                              placeholder = 'Income Sources',
#                              options=get_income_source(),
#                              value='Total Income'),
#                 width={'size':5,'offset':1,'order':1}
#                ),
#         dbc.Col(dcc.Dropdown(id='expense-selector',
#                              placeholder = 'Expense Category',
#                              options = get_expenses_type(),
#                              value = 'Combined Expenses'),
#                width={'size':5,'offest':1,'order':2}
#                ),
#     ], no_gutters=True
#     ),
#     dbc.Row(
#     [
#         dbc.Col(html.Div(className="graph",children=[
#             dcc.Graph(id='pie_chart1',figure={})
            
#         ]),width=6,lg={'size':6,'offset':0,'order':'first'}),
        
#         dbc.Col(html.Div(className="graph",children=[
#             dcc.Graph(id='pie_chart2',figure={})
            
#         ]),width=6,lg={'size':6,'offset':0,'order':'last'}),
#     ]
#     ),
    
#     dbc.Row(
#     [
#         dbc.Col(dcc.Graph(id='savings-chart',figure={}),
#                width=6,lg={'size':6,'offset':0,'order':'first'}
#                ),
#         dbc.Col(dcc.Graph(id='cum-saving',figure={}),
#                width=6,lg={'size':6,'offset':0,'order':'last'}
#                ),
#     ])
# ])

# @dash_app.callback(
#     [Output('pie_chart1','figure'),
#      Output('pie_chart2','figure')],
#     [Input('income-selector','value'),
#      Input('expense-selector','value')]
# )
# def update_graph(income,expense):
#     # if income == "Total Income" or expense == "Combined Expenses":
#     #     pie_fig1 = pie_chart_income()
#     #     pie_fig2 = pie_chart_expense()
#     #     return pie_fig1,pie_fig2
#     # elif income !="Total Income" and expense == "Combined Expenses":
#     #     fig1 = income_chart(income)
#     #     fig2 = pie_chart_expense()
#     #     return fig1,fig2
#     # elif income == "Total Income" and expense !="Combined Expenses":
#     #     fig1 = pie_chart_income()
#     #     fig2 = expenses_chart(expense)
#     #     return fig1,fig2
#     # elif income !="Total Income" and expense !="Combined Expenses":
#     #     fig1 = income_chart(income)
#     #     fig2 = expenses_chart(expense)
#     #     return fig1,fig2
#     # else:
#     #     fig1 = pie_chart_income()
#     #     fig2 = pie_chart_expense()
#     #     return fig1,fig2
#     pie_fig1=None
#     if income=="Total Income" or income==None:
#         pie_fig1=pie_chart_income()
#     else:
#         pie_fig1=income_chart(income)

#     pie_fig2=None
#     if expense=="Combined Expenses" or expense==None:
#         pie_fig2=pie_chart_expense()
#     else:
#         pie_fig2=expenses_chart(expense)
#     return pie_fig1, pie_fig2
    


# @dash_app.callback(
#     [Output('savings-chart','figure'),
#      Output('cum-saving','figure')],
#     [Input('income-selector','value')])
# def update_savings(value):
#     df = get_saving()
#     Date=df['month']
#     # Date=[get_my(i) for i in df['Income_Date']]
#     # if len(df['Expense_Date'])!=0:
#     #     Date = [get_my(i) for i in df['Expense_Date']]
    
#     Savings = df['Savings Per month']
#     Cum_saving = df['Cumulative Savings']
#     figure=None
#     defx=[1,2,3,4]
#     defy=[0,0,0,0]
#     figure = go.Figure(
#         data = [
#                go.Bar(x=defx,y=defy, marker_color='#14bf98')
#         ],
#         layout=go.Layout(
#             title='<b>No Savings Data</b>',
#             showlegend=False,
#             paper_bgcolor='rgba(0,0,0,0)',
#             plot_bgcolor='rgba(0,0,0,0)'
#         )
#     )
    
#     if len(Savings)!=0:
#         figure = go.Figure(
#             data = [
#                 go.Bar(x=Date,y=Savings,text=int(Savings),textposition='auto', marker_color=' #14bf98')
#             ],
#             layout=go.Layout(
#                 title='<b>Amount Saved Per Month</b>',
#                 showlegend=False,
#                 paper_bgcolor='rgba(0,0,0,0)',
#                 plot_bgcolor='rgba(0,0,0,0)'
#             )
#         )
#     figure2 = go.Figure(
#         data = [
#                go.Bar(x=defx,y=defy,marker_color=' #14bf98')
#         ],
#         layout=go.Layout(
#             title='<b>No Cumulative Savings Data</b>',
#             showlegend=False,
#             paper_bgcolor='rgba(0,0,0,0)',
#             plot_bgcolor='rgba(0,0,0,0)'
#         )
#     )

#     if len(Cum_saving)!=0:
#         figure2 = go.Figure(
#             data = [
#                 go.Bar(x=Date,y=Cum_saving,text=int(Cum_saving),textposition='auto',marker_color=' #14bf98')
#             ],
#             layout=go.Layout(
#                 title='<b>Net Savings After Each Month</b>',
#                 showlegend=False,
#                 paper_bgcolor='rgba(0,0,0,0)',
#                 plot_bgcolor='rgba(0,0,0,0)'
#             )
#         )

    
    
#     return figure,figure2

# @app.route('/dashboard/<id>')
# @login_required
# def render_tracker(id):
#     global cur_user
#     cur_user=id
#     return redirect('/tracker/')