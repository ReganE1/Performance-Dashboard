#%%
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash
import numpy
from datetime import date, timedelta, datetime
from common.common_module import *
import plotly.express as px
from xlsxwriter.utility import xl_rowcol_to_cell
#from dash_extensions.snippets import send_bytes
import plotly.graph_objects as go
from Portfolio_Main.PORTFOLIO_LIST import runDenodo_All_Portfolio
from Portfolio_Main.PORTFOLIO_DETAIL import runDenodo_Portfolio_Detail
from Portfolio_Main.PORTFOLIO_PERFORMANCE import runDenodo_Portfolio_Performance
from Portfolio_Main.PORTFOLIO_HOLDINGS import runDenodo_Portfolio_Holdings
from Portfolio_Main.PORTFOLIO_CHARACTERISTICS import runDenodo_Portfolio_Characteristics

dash.register_page(__name__)

#%%
today = date.today()
first = today.replace(day=1)
last_month = first - timedelta(days=1)
#out = date(last_month)
df_port = runDenodo_All_Portfolio()
options_dict_port = dict(zip(df_port['reporting_name_lookup'], df_port['internal_account_code']))

portfolio_id = "3774"
#z = "2023-02-28"
y = "USD"

#%%
#layout
layout = html.Div([
    html.H1(children='Portfolio Dashboard', style={'textAlign':'center'}),
    dcc.Dropdown(
        options=[{'label':reporting_name_lookup, 'value':internal_account_code} for reporting_name_lookup,internal_account_code in options_dict_port.items()],
        value = 'ASE', 
        id='dropdown-selection'),
    html.Div(id='dd-output-container'),
    dcc.DatePickerSingle(
        id='portfolio-date-picker-single',
        min_date_allowed=date(1991, 1, 10),
        max_date_allowed=last_month,
        initial_visible_month=last_month,
        date=last_month
    ),
    html.Div(id='portfolio-output-container-date-picker-single'),
    html.Div(children=[
        dash_table.DataTable(
            id = "portfolio_detail_table",
            page_size=6, 
            style_as_list_view=True,
            style_data = {
                'whiteSpace':'normal',
                'height': 'auto'
            },
            style_header={
                'fontWeight': 'bold'
            },
            style_cell={
                'height':'auto',
                'minWidth':'180px', 'width': '180px', 'maxWidth': '180px',
                'whiteSpace': 'normal',
                'textAlign': 'left'
            },
            style_cell_conditional=[
                {'if': {'column_id': 'Composite Name'},
                    'width': '40%'}
                #{'if':{'column_id':}}
            ],
            fill_width = True),
        html.Div(id='portfolio-curr-output-container',style={'display':'none'}),
        html.Div(id='portfolio-id-output-container',style={'display':'none'}),
        dash_table.DataTable(
            id = "portfolio_performance_table",
            page_size=10, 
            #style_as_list_view=True,
            style_data = {
                'whiteSpace':'normal',
                'height': 'auto'
            },
            style_header={
                'fontWeight': 'bold'
            },
            style_cell={
                'height':'auto',
                'minWidth':'180px', 'width': '180px', 'maxWidth': '180px',
                'whiteSpace': 'normal',
            },
            style_cell_conditional=[
                {'if': {'column_id': 'Period'},
                    'width': '40%', 'textAlign':'left'}
            ],
            fill_width = True),
            ],
        style={'width': '25%', 'display':'inline_block', 'vertical_align': 'top', 'padding':'10px'}),
    html.Div(children=[
        dash_table.DataTable(
            id = "portfolio_holdings_table",
            page_size=10
            ),
        dash_table.DataTable(
            id = "portfolio_characteristics_table",
            page_size=10
            )
        ],
        style={'width': '25%', 'display':'inline_block', 'vertical_align': 'top', 'padding':'10px'}),
    ],
style= {'width':'100%','display':'grid'})

@callback(
    Output('portfolio-output-container-date-picker-single', 'children'),
    Input('portfolio-date-picker-single', 'date'))

#%%
#Portfolio Details

@callback(
    Output(component_id='portfolio_detail_table', component_property='data'),
    Input(component_id = 'dropdown-selection', component_property='value')
)
def portfolio_details_data(col_chosen):
    df = runDenodo_Portfolio_Detail(internal_account_id = col_chosen)
    df_out = df.to_dict('records')
    return df_out

@callback(
    Output(component_id='portfolio-curr-output-container', component_property='value'),
    Input(component_id = 'dropdown-selection', component_property='value')
)
def portfolio_details_data(col_chosen):
    df = runDenodo_Portfolio_Detail(col_chosen)
    df_out = df.loc[0,'Account Reporting Currency']
    return df_out


@callback(
    Output(component_id='portfolio-id-output-container', component_property='value'),
    Input(component_id = 'dropdown-selection', component_property='value')
)
def portfolio_details_data(col_chosen):
    df = runDenodo_Portfolio_Detail(col_chosen)
    df_out = df.loc[0,'Portfolio ID']
    out = str(df_out)
    return out

#%%
#Portfolio Performance
@callback(
    Output(component_id='portfolio_performance_table', component_property='data'),
    Input(component_id = 'portfolio-id-output-container', component_property='value'),
    Input(component_id = 'portfolio-date-picker-single', component_property='date'),
    Input(component_id = 'portfolio-curr-output-container', component_property='value')
)
def portfolio_details_data(port_id,date_chosen,port_curr):
    periods = ['MONTH','quarter','YTD','1 Year Rolling','3 Yrs Annualised','5 Yrs Annualised','7 Yrs Annualised','10 Yrs Annualised','15 Yrs Annualised','20 Yrs Annualised','25 Yrs Annualised','Since Inception','Since Inception Annualised']
    df = runDenodo_Portfolio_Performance(portfolio_id=port_id,reporting_currency=port_curr,valuation_date=date_chosen)
    sub_select = df[['period_name', 'gross_return', 'net_return', 'benchmark_return_1', 'relative_return']]
    data_out = sub_select.rename(columns={'period_name':'Period', 'gross_return':'Gross Perfomance', 'net_return':'Net Performance','benchmark_return_1':'Index Performance','relative_return':'Relative Performance'})
    out = data_out.loc[data_out['Period'].isin(periods)]
    output = out.to_dict('records')
    return output

#%%
#Portfolio Top 10 Holdings
@callback(
    Output(component_id='portfolio_holdings_table', component_property='data'),
    Input(component_id = 'portfolio-id-output-container', component_property='value'),
    Input(component_id = 'portfolio-date-picker-single', component_property='date')
)
def portfolio_details_data(port_id,date_chosen):
    df = runDenodo_Portfolio_Holdings(portfolio_id=port_id,valuation_date=date_chosen)
    filtered = df.sort_values(by='percentage_of_fund', ascending=False).head(10)
    sub_select = filtered[['security_short_name', 'country', 'percentage_of_fund']]
    data_out = sub_select.rename(columns={'security_short_name':'Security Name', 'country':'Country', 'percentage_of_fund':'Portfolio Weight'})
    output = data_out.to_dict('records')
    return output

#%%
#Portfolio Characteristics
@callback(
    Output(component_id='portfolio_characteristics_table', component_property='data'),
    #Output(component_id='portfolio_characteristics_table', component_property='columns'),
    Input(component_id = 'portfolio-id-output-container', component_property='value'),
    Input(component_id = 'portfolio-date-picker-single', component_property='date')
)
def portfolio_characteristics_data(port_id,date_chosen):
    df = runDenodo_Portfolio_Characteristics(portfolio_id=port_id,valuation_date=date_chosen)
    #sub_select = df[['Statistic', 'Portfolio', 'Index']]
    data_out = df.rename(columns={'index':'Statistics'})
    output = data_out.to_dict('records')
    #columns = [{'name': col, 'id': col} for col in df.columns]
    return output