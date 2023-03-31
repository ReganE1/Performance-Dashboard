#%%
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash
from common.common_module import *
import plotly.express as px
from Composite_Main.CUMULATIVE_COMPOSITE import cumulative_comp_perf_output
from Composite_Main.COMPOSITE_LIST import composite_list
from Composite_Main.COMPOSITE_DISCLOSURE import composite_disclosure
import plotly.graph_objects as go

dash.register_page(__name__)
df_ccp = cumulative_comp_perf_output
df_comp = composite_list
dff_comp = composite_list.composite_name
df_cdisc = composite_disclosure

#%%
#Composite Cumulative Performance
dff_ccp =df_ccp.sort_values(by='period_ending')
fig =go.Figure()
#traces
fig.add_trace(
    go.Scatter(
    x=dff_ccp.period_ending, y=dff_ccp.indexed_composite_performance, name = 'Composite Gross Performance', line = dict(color='firebrick', width = 4)))
fig.add_trace(
    go.Scatter(
    x=dff_ccp.period_ending, y=dff_ccp.indexed_composite_net_performance, name = 'Composite Net Performance', line = dict(color='royalblue', width = 4)))
fig.add_trace(
    go.Scatter(
    x=dff_ccp.period_ending, y=dff_ccp.indexed_benchmark_performance, name = 'Benchmark Performance', line = dict(color='darkgreen', width = 4)))


fig.update_layout(title='Cumulative Composite Performance',
                  xaxis_title = 'Year',
                  yaxis_title='Return')
fig.show()


#%%
#Composite & Fee Scale Description
dff_cdisc = df_cdisc.composite_description + '\n' + df_cdisc.fee_scale_description

#layout
layout = html.Div([
    html.H1(children='Composite Dashboard', style={'textAlign':'center'}),
    dcc.Dropdown(
        options=[{'label':i, 'value':i} for i in dff_comp.unique()],
        value = 'International Equity', 
        id='dropdown-selection'),
    html.Div(id='dd-output-container'),
    dcc.Graph(
        id="cumulative_composite",
        figure=fig,
        style={'width':'50%', 'height': '30%'}),
    html.H3(children='Composite Disclosure',style={'textAlign':'left'}),
    html.Div(df_cdisc.composite_description, style = {'colour': 'black', 'fontSize': 36, 'width':'50%'}),
    html.H3(children='Fee Scale',style={'textAlign':'left'}),
    html.Div(df_cdisc.fee_scale_description, style = {'colour': 'black', 'fontSize': 36, 'width':'50%'})
])

@callback(
    Output('dd-output-container', 'children'),
    Input('dropdown-selection', 'value')
)
def update_output(value):
    return f'You have selected {value}'


