#%%
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash
from common.common_module import *
import plotly.express as px
from Composite_Main.CUMULATIVE_PERFORMANCE import runDenodo_Cumulative_Composite_Performance, runDenodo_Composite_Performance
from Composite_Main.COMPOSITE_LIST import composite_list
from Composite_Main.COMPOSITE_DISCLOSURE import runDenodo_Composite_Disclosure
from Composite_Main.COMPOSITE_INFO import runDenodo_Composite_Details
import plotly.graph_objects as go

dash.register_page(__name__)

df_comp = composite_list
options_dict = dict(zip(df_comp['composite_name'], df_comp['composite_code']))
dff_comp = composite_list.composite_name
#df_cdisc = composite_disclosure


#x = "INT_EQ"
z = "2023-02-28"
y = "USD"

#%%
#layout
layout = html.Div([
    html.H1(children='Composite Dashboard', style={'textAlign':'center'}),
    dcc.Dropdown(
        options=[{'label':composite_name, 'value':composite_code} for composite_name,composite_code in options_dict.items()],
        value = 'INT_EQ', 
        id='dropdown-selection'),
    html.Div(id='dd-output-container'),
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
        style={'width': '20%', 'display':'inline-block', 'padding':'10px'}),
    html.Div(children=[
        dcc.Graph(
            id="cumulative_composite",
            figure={},
            #style={'width':'50%', 'height': '40%', 'display':'inline-block', 'padding':'10px'}
            ),
        ],
        style={'width':'50%', 'height': 'auto', 'display':'inline-block', 'padding':'10px'}
        ),
    html.H3(children='Composite Disclosure',style={'textAlign':'left'}),
    html.Div(id = "composite_description", children= {}, style = {'colour': 'black', 'fontSize': 36, 'width':'50%'}),
    html.H3(children='Fee Scale',style={'textAlign':'left'}),
    html.Div(id = "fee_scale_description", children = {}, style = {'colour': 'black', 'fontSize': 36, 'width':'50%'})
],
style= {'width':'100%','display':'inline-block'})

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

#Composite Performance

@callback(
    Output(component_id='composite_performance_table', component_property='data'),
    Input(component_id = 'dropdown-selection', component_property='value')
)
def composite_details_data(col_chosen):
    df = runDenodo_Composite_Performance(composite_code=col_chosen,reporting_currency=y,valuation_date=z)
    df_out = df.to_dict('records')
    return df_out


#%%
#Composite Cumulative Performance

@callback(
    Output(component_id='cumulative_composite', component_property='figure'),
    Input(component_id = 'dropdown-selection', component_property='value')
)
def cumulative_fig_ccpure(col_chosen):
    df_ccp = runDenodo_Cumulative_Composite_Performance(composite_code=col_chosen,reporting_currency=y,valuation_date=z)
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
    Input(component_id = 'dropdown-selection', component_property='value')
)

def composite_description_update(col_chosen):
    df_cdisc = runDenodo_Composite_Disclosure(composite_code=col_chosen,reporting_currency=y,valuation_date=z)
    children = df_cdisc.composite_description
    return children

@callback(
    Output(component_id='fee_scale_description', component_property='children'),
    Input(component_id = 'dropdown-selection', component_property='value')
)

def fee_scale_description_update(col_chosen):
    df_cdisc_f = runDenodo_Composite_Disclosure(composite_code=col_chosen,reporting_currency=y,valuation_date=z)
    children = df_cdisc_f.fee_scale_description
    return children
