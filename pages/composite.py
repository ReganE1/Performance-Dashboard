#%%
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash
from common.common_module import *
import plotly.express as px
from Composite_Main.CUMULATIVE_COMPOSITE import runDenodo_Cumulative_Composite_Performance
from Composite_Main.COMPOSITE_LIST import composite_list
from Composite_Main.COMPOSITE_DISCLOSURE import composite_disclosure
import plotly.graph_objects as go

dash.register_page(__name__)

df_comp = composite_list
options_dict = dict(zip(df_comp['composite_name'], df_comp['composite_code']))
dff_comp = composite_list.composite_name
df_cdisc = composite_disclosure

x = "INT_EQ"
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
    dcc.Graph(
        id="cumulative_composite",
        figure={},
        style={'width':'50%', 'height': '30%'}),
    html.H3(children='Composite Disclosure',style={'textAlign':'left'}),
    html.Div(df_cdisc.composite_description, style = {'colour': 'black', 'fontSize': 36, 'width':'50%'}),
    html.H3(children='Fee Scale',style={'textAlign':'left'}),
    html.Div(df_cdisc.fee_scale_description, style = {'colour': 'black', 'fontSize': 36, 'width':'50%'})
])
"""
@callback(
    Output('dd-output-container', 'children'),
    Input('dropdown-selection', 'value')
)
def update_output(value):
    composite_code_value = df_comp.query('composite_name'==value,)['composite_code']
    return composite_code_value
    
comp_value = update_output('dd-output-container')
"""

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
#dff_cdisc = df_cdisc.composite_description + '\n' + df_cdisc.fee_scale_description




