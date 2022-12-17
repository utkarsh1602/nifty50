from dash import dcc
from dash import html
from utils import constants
import plotly.graph_objects as go


def get_layout(**kwargs):
    layout = [
        html.Br(),
        html.Hr(),
        html.Br(),
        html.H3('Select the Ticker and Time Range for Analysis'),
        html.Hr(),
        html.Div(
            id='filters', children=[
                html.Div(children=[
                    html.Div(id='index', children=[dcc.Dropdown(
                        id='ticker', value=kwargs.get('ticker'), options=constants.TICKERS, placeholder='Ticker'
                    )], style={'margin': 'auto', 'width': 200,
                               'padding': '10px', 'float': 'left', 'color': 'Black'}),
                    html.Div(id='graph-type', children=[dcc.Dropdown(
                        id='type', value=kwargs.get('graph_type', 1), options={1: 'Candle Stick', 2: 'Scatter'}
                    )], style={'margin': 'auto', 'width': 200,
                               'padding': '10px', 'float': 'left', 'color': 'Black'}),
                    html.Div(id='timeframe', children=[dcc.Dropdown(
                        id='time', value=kwargs.get('timeframe', 180),
                        options={7: '1week', 30: '1m', 180: '6m', 365: '1y', 730: '2y', 1095: '3y', 1825: '5Y'}
                    )], style={'margin': 'auto', 'width': 200,
                               'padding': '10px', 'float': 'left', 'color': 'Black'}),
                    html.Label('Select the Moving Averages', htmlFor='moving-averages'), html.Br(),
                    html.Div(id='moving-averages', children=[
                        dcc.Checklist(id='mv-avg',
                                      value=kwargs.get('mv_avg', []),
                                      options=[{'label': '50 Days', 'value': 50},
                                               {'label': '100 Days', 'value': 100},
                                               {'label': '200 Days', 'value': 200}],
                                      inline=True
                                      )
                    ], style={'margin': 'auto', 'width': 300,
                              'padding': '10px', 'float': 'left'}),
                    html.Br(),
                    html.Div(id='volume', children=[
                        dcc.Checklist(id='vol',
                                      value=kwargs.get('vol', []),
                                      options=[{'label': 'Volume', 'value': True}])
                    ], style={'margin': 'auto', 'width': 100,
                              'padding': '10px', 'float': 'right'})
                ])
            ]
        ),
        html.Br(),
        html.Div(
            id='main-graph', children=[
                dcc.Graph(figure=go.Figure())
            ],
            style={'margin': 'auto', 'padding': '5px', 'width': '1250px',
                   'float': 'left'}
        ),
        html.Br(),
        html.Div(
            id='market-info', children=[
                html.Div(children=[
                    html.H3('Current Market Price'),
                ],
                    style={'margin': '50px', 'border': '2px solid', 'text-align': 'center',
                           'border-radius': '10%', 'height': '200px', 'width': '200px', 'float': 'left'}
                ),
                html.Div(children=[
                    html.H3('Percentage Return on Stock'),
                ],
                    style={'margin': '50px', 'border': '2px solid', 'text-align': 'center',
                           'border-radius': '10%', 'height': '200px', 'width': '200px', 'float': 'left'}
                ),
                html.Div(children=[
                    html.H3('Volatility of Stock (STD)'),
                ],
                    style={'margin': '50px', 'border': '2px solid', 'text-align': 'center',
                           'border-radius': '10%', 'height': '200px', 'width': '200px', 'float': 'left'}
                ),
                html.Div(children=[
                    html.H3('Total Volume of Stock Traded'),
                ],
                    style={'margin': '50px', 'border': '2px solid', 'text-align': 'center',
                           'border-radius': '10%', 'height': '200px', 'width': '200px', 'float': 'left'}
                )
            ],
            style={'margin': 'auto', 'padding': '10px', 'overflow-y': 'hidden'}
        )]

    return layout
