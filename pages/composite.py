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
from Composite_Main.CUMULATIVE_PERFORMANCE import runDenodo_Cumulative_Composite_Performance, runDenodo_Composite_Performance, runDenodo_Composite_Performance_Extract
from Composite_Main.COMPOSITE_LIST import composite_list
from Composite_Main.COMPOSITE_DISCLOSURE import runDenodo_Composite_Disclosure
from Composite_Main.COMPOSITE_INFO import runDenodo_Composite_Details
from Composite_Main.COMPOSITE_BULL_BEAR import runDenodo_Composite_Defensive_Characteristics_Month, runDenodo_Composite_Defensive_Characteristics_Quarter, runDenodo_Composite_Defensive_Characteristics_All,period_list
import plotly.graph_objects as go

dash.register_page(__name__)

#%%
today = date.today()
first = today.replace(day=1)
last_month = first - timedelta(days=1)
#out = date(last_month)
#%%
df_comp = composite_list
options_dict_comp = dict(zip(df_comp['composite_name'], df_comp['composite_code']))
df_period = period_list
#options_dict_period = dict(zip(period_list['period_length']))
#dff_comp = composite_list.composite_name
#df_cdisc = composite_disclosure


#x = "INT_EQ"
#z = "2023-02-28"
y = "USD"

#%%
#layout
layout = html.Div([
    html.H1(children='Composite Dashboard', style={'textAlign':'center'}),
    dcc.Dropdown(
        options=[{'label':composite_name, 'value':composite_code} for composite_name,composite_code in options_dict_comp.items()],
        value = 'INT_EQ', 
        id='dropdown-selection'),
    html.Div(id='dd-output-container'),
    dcc.DatePickerSingle(
        id='date-picker-single',
        min_date_allowed=date(1991, 1, 10),
        max_date_allowed=last_month,
        initial_visible_month=last_month,
        date=last_month
    ),
    html.Div(id='output-container-date-picker-single'),
    html.Div(children=[
        dash_table.DataTable(
            id = "composite_detail_table",
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
        html.Div(id='curr-output-container',style={'display':'none'}),
        dash_table.DataTable(
            id = "composite_performance_table",
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
        dcc.Graph(
            id="cumulative_composite",
            figure={},
            #style={'width':'50%', 'height': '40%', 'display':'inline-block', 'padding':'10px'}
            ),
        ],
        style={'width':'40%', 'height': 'auto', 'display':'inline_block', 'vertical_align': 'top', 'padding':'10px'}
        ),
    html.H3(children='Composite Disclosure',style={'textAlign':'left'}),
    html.Div(id = "composite_description", children= {}, style = {'colour': 'black', 'fontSize': 36, 'width':'50%'}),
    html.H3(children='Fee Scale',style={'textAlign':'left'}),
    html.Div(id = "fee_scale_description", children = {}, style = {'colour': 'black', 'fontSize': 36, 'width':'50%'}),
    html.Div(children =[
        dcc.Dropdown(
            options=[{'label':i, 'value':i} for i in df_period.period_length.unique()],
            value = 'SINCE INCEPTION', 
            id='period-selection'),
        html.Div(id='dd-period-output-container'),
        dcc.RadioItems(options =['Monthly','Quarterly'], value = 'Monthly', id='bull_bear_radio'),
        dcc.Graph(
            id = "bull_bear_graph_quarter",
            figure={}
        ),
        dcc.Graph(
            id = "bull_bear_graph_month",
            figure={},
        ),
        html.Div(children=[
            dash_table.DataTable(
                id = "period_performance",
                ),
            dash_table.DataTable(
                id = "period_count",
                ),
            dash_table.DataTable(
                id = "period_bulls",
                ),
            dash_table.DataTable(
                id = "period_bears",
                )
                ],
            style={'width': '25%', 'display':'grid', 'vertical_align': 'top', 'padding':'10px'}
            ),
        ],
        style={'width':'50%', 'height': 'auto', 'display':'inline-block', 'padding':'10px'}
        ),
    html.Button("Download Excel", id="btn_comp_xlsx"),
    dcc.Download(id="download-dataframe-xlsx")
    ],
style= {'width':'100%','display':'grid'})

@callback(
    Output('output-container-date-picker-single', 'children'),
    Input('date-picker-single', 'date'))

#%%
#Composite Details

@callback(
    Output(component_id='composite_detail_table', component_property='data'),
    Input(component_id = 'dropdown-selection', component_property='value')
)
def composite_details_data(col_chosen):
    df = runDenodo_Composite_Details(col_chosen)
    df_out = df.to_dict('records')
    return df_out

@callback(
    Output(component_id='curr-output-container', component_property='value'),
    Input(component_id = 'dropdown-selection', component_property='value')
)
def composite_reporting_currency(col_chosen):
    df = runDenodo_Composite_Details(col_chosen)
    df_out = df.loc[0,'Composite Currency']
    return df_out


#Composite Performance

@callback(
    Output(component_id='composite_performance_table', component_property='data'),
    Input(component_id = 'dropdown-selection', component_property='value'),
    Input(component_id = 'date-picker-single', component_property='date'),
    Input(component_id = 'curr-output-container', component_property='value')
)
def composite_details_data(col_chosen,date_chosen,comp_curr):
    df = runDenodo_Composite_Performance(composite_code=col_chosen,reporting_currency=comp_curr,valuation_date=date_chosen)
    sub_select = df[['period_length', 'composite_gross_performance', 'composite_net_performance', 'benchmark_performance', 'relative_performance']]
    data_out = sub_select.rename(columns={'period_length':'Period', 'composite_gross_performance':'Gross Perfomance', 'composite_net_performance':'Net Performance','benchmark_performance':'Index Performance','relative_performance':'Relative Performance'})
    df_out = data_out.to_dict('records')
    return df_out


#%%
#Composite Cumulative Performance

@callback(
    Output(component_id='cumulative_composite', component_property='figure'),
    Input(component_id = 'dropdown-selection', component_property='value'),
    Input(component_id = 'date-picker-single', component_property='date'),
    Input(component_id = 'curr-output-container', component_property='value')
)
def cumulative_fig_ccpure(col_chosen, date_chosen,comp_curr):
    df_ccp = runDenodo_Cumulative_Composite_Performance(composite_code=col_chosen,reporting_currency=comp_curr,valuation_date=date_chosen)
    dff_ccp =df_ccp.sort_values(by='period_ending')
    fig_ccp =go.Figure()
    #traces
    fig_ccp.add_trace(
        go.Scatter(
        x=dff_ccp.period_ending, y=dff_ccp.indexed_composite_performance, name = 'Composite Gross Performance', line = dict(color='firebrick', width = 4)))
    fig_ccp.add_trace(
        go.Scatter(
        x=dff_ccp.period_ending, y=dff_ccp.indexed_composite_net_performance, name = 'Composite Net Performance', line = dict(color='royalblue', width = 4)))
    fig_ccp.add_trace(
        go.Scatter(
        x=dff_ccp.period_ending, y=dff_ccp.indexed_benchmark_performance, name = 'Benchmark Performance', line = dict(color='darkgreen', width = 4)))


    fig_ccp.update_layout(title='Cumulative Composite Performance',
                    xaxis_title = 'Year',
                    yaxis_title='Return')
    return fig_ccp


    

#%%
#Composite & Fee Scale Description

@callback(
    Output(component_id='composite_description', component_property='children'),
    Input(component_id = 'dropdown-selection', component_property='value'),
    Input(component_id = 'date-picker-single', component_property='date'),
    Input(component_id = 'curr-output-container', component_property='value')
)

def composite_description_update(col_chosen,date_chosen,comp_curr):
    df_cdisc = runDenodo_Composite_Disclosure(composite_code=col_chosen,reporting_currency=comp_curr,valuation_date=date_chosen)
    children = df_cdisc.composite_description
    return children

@callback(
    Output(component_id='fee_scale_description', component_property='children'),
    Input(component_id = 'dropdown-selection', component_property='value'),
    Input(component_id = 'date-picker-single', component_property='date'),
    Input(component_id = 'curr-output-container', component_property='value')
)

def fee_scale_description_update(col_chosen,date_chosen,comp_curr):
    df_cdisc_f = runDenodo_Composite_Disclosure(composite_code=col_chosen,reporting_currency=comp_curr,valuation_date=date_chosen)
    children = df_cdisc_f.fee_scale_description
    return children


#%%
#Composite Bull Bear Quarter
@callback(
    Output(component_id='bull_bear_graph_quarter', component_property='figure'),
    Input(component_id = 'period-selection', component_property='value'),
    Input(component_id = 'dropdown-selection', component_property='value'),
    Input(component_id = 'date-picker-single', component_property='date'),
    Input(component_id = 'curr-output-container', component_property='value')
)
def quarterly_bull_bear(period_chosen,col_chosen,date_chosen,comp_curr):
    df_bb_quarterly = runDenodo_Composite_Defensive_Characteristics_Quarter(composite_code=col_chosen,reporting_currency=comp_curr,valuation_date=date_chosen,period_length=period_chosen)
    output = df_bb_quarterly.loc[df_bb_quarterly['Data_Point'].isin(['Bull Count','Bear Count', 'Total Quarters'])]
    Column = output['Data_Point'].values.tolist()
    Data = output['Data_Value'].values.tolist()
    fig = go.Figure()
    fig = px.bar(x=Column,y=Data)
    fig.update_layout(title='Quarterly Bull Bear',
                      xaxis_title='',
                    yaxis_title='Count')
    return fig

#%%
#Composite Bull Bear Month
@callback(
    Output(component_id='bull_bear_graph_month', component_property='figure'),
    Input(component_id = 'period-selection', component_property='value'),
    Input(component_id = 'dropdown-selection', component_property='value'),
    Input(component_id = 'date-picker-single', component_property='date'),
    Input(component_id = 'curr-output-container', component_property='value')
)
def monthly_bull_bear(period_chosen,col_chosen,date_chosen,comp_curr):
    df_bb_quarterly = runDenodo_Composite_Defensive_Characteristics_Month(composite_code=col_chosen,reporting_currency=comp_curr,valuation_date=date_chosen,period_length=period_chosen)
    output = df_bb_quarterly.loc[df_bb_quarterly['Data_Point'].isin(['Bull Count','Bear Count', 'Total Months'])]
    Column = output['Data_Point'].values.tolist()
    Data = output['Data_Value'].values.tolist()
    fig = go.Figure()
    fig = px.bar(x=Column,y=Data)
    fig.update_layout(title='Monthly Bull Bear',
                      xaxis_title='',
                    yaxis_title='Count')
    return fig


#%%
#bull bear chart radio buttons logic - not shown on month and always default to monthly
@callback(
    Output(component_id='bull_bear_radio', component_property='style'),
    Output(component_id='bull_bear_radio', component_property='value'),
    Input(component_id='date-picker-single', component_property='date')
)
def bull_bear_radio_visibility(date_chosen):
    date = datetime.strptime(date_chosen,'%Y-%m-%d')
    month = date.month
    if month in (1,2,4,5,7,8,10,11):
        return {'display':'none'}, 'Monthly'
    else: return {'display':'inline'}, 'Monthly'


#Chart visibility rules

@callback(
    Output(component_id='bull_bear_graph_quarter', component_property='style'),
    Input(component_id='bull_bear_radio', component_property='value')
)
def quarterly_bull_bear_visibility(type):
    if type == 'Quarterly':
        return {'display':'block'}
    else: return {'display':'none'}

@callback(
    Output(component_id='bull_bear_graph_month', component_property='style'),
    Input(component_id='bull_bear_radio', component_property='value')
)
def quarterly_bull_bear_visibility(type):
    if type == 'Monthly':
        return {'display':'block'}
    else: return {'display':'none'}

#%%
#period performance - missing relative


@callback(
    Output(component_id='period_performance', component_property='data'),
    Input(component_id = 'period-selection', component_property='value'),
    Input(component_id = 'dropdown-selection', component_property='value'),
    Input(component_id = 'date-picker-single', component_property='date'),
    Input(component_id = 'curr-output-container', component_property='value')
)
def period_performance_table(period_chosen,col_chosen,date_chosen,comp_curr):
    df = runDenodo_Composite_Defensive_Characteristics_All(composite_code=col_chosen,reporting_currency=comp_curr,valuation_date=date_chosen,period_length=period_chosen)
    output = df.loc[df['data'].isin(['composite_performance','benchmark_performance', 'cpi_performance'])]
    df_out = output.to_dict('records')
    return df_out

@callback(
    Output(component_id='period_count', component_property='data'),
    Input(component_id = 'period-selection', component_property='value'),
    Input(component_id = 'dropdown-selection', component_property='value'),
    Input(component_id = 'date-picker-single', component_property='date'),
    Input(component_id='bull_bear_radio', component_property='value'),
    Input(component_id = 'curr-output-container', component_property='value')
)
def period_performance_table(period_chosen,col_chosen,date_chosen, type, comp_curr):
    df = runDenodo_Composite_Defensive_Characteristics_All(composite_code=col_chosen,reporting_currency=comp_curr,valuation_date=date_chosen,period_length=period_chosen)
    if type == 'Monthly':
        period_performance_rows = ['bull_count_month','bear_count_month', 'total_months']
    else: period_performance_rows = ['bull_count_quarter','bear_count_quarter', 'total_quarters']
    output = df.loc[df['data'].isin(period_performance_rows)]
    df_out = output.to_dict('records')
    return df_out
    
@callback(
    Output(component_id='period_bulls', component_property='data'),
    Input(component_id = 'period-selection', component_property='value'),
    Input(component_id = 'dropdown-selection', component_property='value'),
    Input(component_id = 'date-picker-single', component_property='date'),
    Input(component_id='bull_bear_radio', component_property='value'),
    Input(component_id = 'curr-output-container', component_property='value')
)
def period_performance_table(period_chosen,col_chosen,date_chosen, type, comp_curr):
    df = runDenodo_Composite_Defensive_Characteristics_All(composite_code=col_chosen,reporting_currency=comp_curr,valuation_date=date_chosen,period_length=period_chosen)
    if type == 'Monthly':
        period_bulls_rows = ['composite_performance_bull_month','benchmark_performance_bull_month']
    else: period_bulls_rows = ['composite_performance_bull_quarter','benchmark_performance_bull_quarter']
    output = df.loc[df['data'].isin(period_bulls_rows)]
    df_out = output.to_dict('records')
    return df_out

@callback(
    Output(component_id='period_bears', component_property='data'),
    Input(component_id = 'period-selection', component_property='value'),
    Input(component_id = 'dropdown-selection', component_property='value'),
    Input(component_id = 'date-picker-single', component_property='date'),
    Input(component_id='bull_bear_radio', component_property='value'),
    Input(component_id = 'curr-output-container', component_property='value')
)
def period_performance_table(period_chosen,col_chosen,date_chosen, type,comp_curr):
    df = runDenodo_Composite_Defensive_Characteristics_All(composite_code=col_chosen,reporting_currency=comp_curr,valuation_date=date_chosen,period_length=period_chosen)
    if type == 'Monthly':
        period_bulls_rows = ['composite_performance_bear_month','benchmark_performance_bear_month']
    else: period_bulls_rows = ['composite_performance_bear_quarter','benchmark_performance_bear_quarter']
    output = df.loc[df['data'].isin(period_bulls_rows)]
    df_out = output.to_dict('records')
    return df_out


#%%
#excel download
periodic_periods = ['1 YEAR ROLLING',
'10 YEAR ANNUALISED',
'10 YEAR ROLLING',
'15 YEAR ANNUALISED',
'15 YEAR ROLLING',
'2 YEAR ANNUALISED',
'2 YEAR ROLLING',
'20 YEAR ANNUALISED',
'20 YEAR ROLLING',
'25 YEAR ANNUALISED',
'25 YEAR ROLLING',
'3 YEAR ANNUALISED',
'3 YEAR ROLLING',
'4 YEAR ANNUALISED',
'4 YEAR ROLLING',
'5 YEAR ANNUALISED',
'5 YEAR ROLLING',
'7 YEAR ANNUALISED',
'7 YEAR ROLLING',
'SINCE INCEPTION',
'SINCE INCEPTION ANNUALISED',
'YTD']

@callback(
    Output("download-dataframe-xlsx","data"),
    Input("btn_comp_xlsx", "n_clicks"),
    Input(component_id = 'dropdown-selection', component_property='value'),
    Input(component_id = 'date-picker-single', component_property='date'),
    Input(component_id = 'curr-output-container', component_property='value'),
    prevent_inital_call=True
)
def composite_returns_download(n_clicks,col_chosen,date_chosen,comp_curr):
    if n_clicks is None:
        return dash.no_update
    else:
        df = runDenodo_Composite_Performance_Extract(composite_code=col_chosen,reporting_currency=comp_curr,valuation_date=date_chosen)
        def to_xlsx(bytes_io):
            output_periodic = df.loc[df['period_length'].isin(periodic_periods)]
            output_annual = df.loc[df['period_length'].isin(['YEAR'])]
            output_quarterly = df.loc[df['period_length'].isin(['QUARTER'])]
            output_monthly = df.loc[df['period_length'].isin(['MONTH'])]
            with pd.ExcelWriter(bytes_io) as writer:
                output_periodic.to_excel(writer, sheet_name="Periodic Returns", index= False)
                output_annual.to_excel(writer, sheet_name="Annual Returns", index= False)
                output_quarterly.to_excel(writer, sheet_name="Quarterly Returns", index= False)
                output_monthly.to_excel(writer, sheet_name="Monthly Returns", index= False)
        return dcc.send_bytes(to_xlsx, "Download_Composite_Returns.xlsx")
    
