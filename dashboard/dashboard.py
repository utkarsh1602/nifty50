from dash import Dash
from dash import Input, Output
from dash import dcc
from dash import html

import helper
import prediction_page
import tech_analysis_page

app = Dash(__name__)

app.layout = html.Div(
    id='main-div', children=[
        dcc.Tabs(id='all-tabs', children=[
            dcc.Tab(label='Technical Analysis', value='tab-1'),
            dcc.Tab(label='Stock Prediction', value='tab-2'),
            dcc.Tab(label='Correlation Map', value='tab-3'),
            dcc.Tab(label='Stock News', value='tab-4')
        ], style={'color': 'Black'}),
        html.Div(id='tab-content')
    ],
    style={'padding': '10px', 'overflow': 'hidden',
           'font-family': 'Arial', 'font-size': '15px'}
)


@app.callback(
    Output(component_id='tab-content', component_property='children'),
    Input(component_id='all-tabs', component_property='value'),
)
def update_tab(tab):
    if tab == 'tab-1':
        return tech_analysis_page.layout
    if tab == 'tab-2':
        return prediction_page.layout


@app.callback(
    Output(component_id='main-graph', component_property='children'),
    Input(component_id='ticker', component_property='value'),
    Input(component_id='type', component_property='value'),
    Input(component_id='time', component_property='value'),
    Input(component_id='mv-avg', component_property='value'),
    Input(component_id='vol', component_property='value'),
)
def update_chart(*args):
    ticker = args[0]
    graph_type = int(args[1])
    timeframe = int(args[2])
    mv_avg = args[3]
    vol = args[4][0] if args[4] else False
    graph = helper.get_graph(ticker=ticker, type=graph_type, days=timeframe, mv_avg=mv_avg, vol=vol)
    data = dcc.Graph(figure=graph)
    return [data]


@app.callback(
    Output(component_id='market-info', component_property='children'),
    Input(component_id='ticker', component_property='value'),
    Input(component_id='time', component_property='value'),
    prevent_initial_call=True
)
def update_info(*args):
    ticker = args[0]
    timeframe = int(args[1])
    style = {'margin': '50px', 'border': '2px solid', 'text-align': 'center',
             'border-radius': '10%', 'height': '200px', 'width': '200px', 'float': 'left'}
    mp, roi, std, total_vol = helper.get_market_info(ticker=ticker, time=timeframe)
    data = [html.Div(children=[
        html.H3('Current Market Price'),
        html.P(mp)
    ],
        style=style
    ),
        html.Div(children=[
            html.H3('Percentage Return on Stock'),
            html.P('{}%'.format(roi))
        ],
            style=style
        ),
        html.Div(children=[
            html.H3('Volatility of Stock (STD)'),
            html.P(std)
        ],
            style=style
        ),
        html.Div(children=[
            html.H3('Total Volume of Stock Traded'),
            html.P(total_vol)
        ],
            style=style
        )]
    return data


if __name__ == '__main__':
    app.run(debug=True)
