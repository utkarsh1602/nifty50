from dash import html
import helper


def get_status(value):
    if value == 0:
        return 'Hold', '#99d6ff'
    if value == 1:
        return 'Buy', '#aaff80'
    if value == -1:
        return 'Sell', '#ff8080'


def get_all_data():
    all_predictions = helper.get_all_prediction()
    data = []
    for key, value in all_predictions.items():
        val, color = get_status(value)
        a = html.Tr(children=[html.Td(key, style={'background-color': '#c2c2a3', 'padding': '5px', 'border': '1px solid'}),
                              html.Td(val, style={'background-color': color, 'padding': '5px', 'border': '1px solid'})])
        data.append(a)

    return data


layout = [
    html.Br(),
    html.Hr(),
    html.Br(),
    html.H1('Prediction for all NIFTY50 stocks', style={'text-align': 'center'}),
    html.Hr(),
    html.Br(),
    html.Table(id='all-stocks', children=[
        html.Thead(children=[
            html.Tr(children=[
                html.Th('Stock', style={'padding': '5px', 'border': '1px solid'}),
                html.Th('Prediction', style={'padding': '5px', 'border': '1px solid'})
            ])
        ], style={'background-color': '#ffff00'}),
        html.Tbody(children=get_all_data())
    ], style={'padding': '5px', 'width': '100%',
              'border': '2px solid',
              'text-align': 'center'}
               )
]
