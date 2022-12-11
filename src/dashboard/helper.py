import pickle

import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
import pandas
import datetime
import pandas as pd

import constants


def get_graph(ticker, **kwargs):
    if ticker:
        fp = open('../historical_data/{}.csv'.format(ticker), 'r')
        df = pandas.read_csv(fp)
        x = get_time_series(time_series=df['Date'], days=kwargs.get('days', 30))
        data = df[df['Date'].isin(x)]
        graph_list = []
        main_graph = select_type_of_graph(data, graph_type=kwargs.get('type'))
        graph_list.append(main_graph)

        if kwargs.get('mv_avg'):
            for avg in kwargs.get('mv_avg'):
                moving_avg_graph = get_moving_average_graph(data=data, days=avg)
                graph_list.append(moving_avg_graph)

        if kwargs.get('vol'):
            volume_graph = get_volume_traded_graph(data)
            graph_list.append(volume_graph)

        graph = go.Figure(graph_list)
        graph.update_layout(xaxis_rangeslider_visible=False, height=600, width=1200,
                            plot_bgcolor=constants.BG_COLOR, paper_bgcolor=constants.BG_COLOR,
                            font_color='White')
        return graph
    else:
        return go.Figure().update_layout(xaxis_rangeslider_visible=False, height=600, width=1200,
                                         plot_bgcolor=constants.BG_COLOR, paper_bgcolor=constants.BG_COLOR,
                                         font_color='White')


def get_time_series(time_series, days):
    time_diff = datetime.datetime.now() - datetime.timedelta(days)
    time_s = list(filter(lambda d: datetime.datetime.strptime(d, '%Y-%m-%d') > time_diff,
                         list(time_series)))
    return time_s


def select_type_of_graph(data, graph_type):
    if graph_type == 1:
        return go.Candlestick(
            x=data['Date'],
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Daily Change'
        )
    else:
        return go.Scatter(
            x=data['Date'],
            y=data['Adj Close'],
            name='Daily Change'
        )


def get_moving_average_graph(data, days):
    avg_close = data['Adj Close'].rolling(window=days, min_periods=1).mean()
    return go.Scatter(
        x=data['Date'],
        y=avg_close,
        name='{} day mv'.format(days)
    )


def get_volume_traded_graph(data):
    min_close = data['Close'].min() - 10
    data['Volume'] = MinMaxScaler(feature_range=(0, 10)).fit_transform(data[['Volume']])
    return go.Bar(
        x=data['Date'], y=data['Volume'], base=min_close, name='Volume Traded'
    )


def get_market_info(ticker, time):
    mp, roi, std, total_vol = -1, -1, -1, -1
    if ticker:
        fp = open('../historical_data/{}.csv'.format(ticker), 'r')
        df = pandas.read_csv(fp)
        x = get_time_series(time_series=df['Date'], days=time)
        data = df[df['Date'].isin(x)]
        mp = data['Close'].iloc[-1]
        roi = get_return_on_stock(data)
        std = data['Close'].std()
        total_vol = data['Volume'].sum()

    return round(mp, 2), round(roi, 2), round(std, 2), round(total_vol, 2)


def get_return_on_stock(data):
    return ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100


def clean_dataframe(df):
    df.fillna(0)
    df.dropna()
    return df


def combine_all_stock_data(tickers):
    new_df = pd.DataFrame()
    for ticker in tickers:
        fp = open('../historical_data/{}.csv'.format(ticker), 'r')
        df = pd.read_csv(fp)
        new_df[ticker] = df[['Adj Close']].rolling(100, min_periods=1).mean()
    new_df = clean_dataframe(new_df)
    return new_df


def get_all_prediction():
    new_df = combine_all_stock_data(constants.TICKERS)
    x = new_df[[ticker for ticker in constants.TICKERS]]
    x = x.pct_change()
    x = x.iloc[[-1]]
    predictions = dict()
    for ticker in constants.TICKERS:
        try:
            path = '../classifier_models/{}'.format(ticker)
            fp = open(path, 'rb')
            model = pickle.load(fp)
            predictions[ticker] = eval(str(model.predict(x)))[0]
        except Exception as e:
            print(e)

    return predictions
