from fetch_data import HistoricalData
import constants as const
import pandas as pd
import pickle
import os
from collections import Counter

from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import train_test_split


def clean_dataframe(df):
    df.fillna(0, inplace=True)
    df.dropna(inplace=True)


def update_all_stock_data():
    obj = HistoricalData()
    obj.get_all_data()


def combine_all_stock_data(tickers):
    for ticker in tickers:
        df = pd.read_csv('{}/{}.csv'.format(const.HISTORICAL_DATA_BASE, ticker))
        new_df[ticker] = df[['Adj Close']].rolling(100, min_periods=1).mean()
    clean_dataframe(new_df)


def cal_per_change(ticker, days=7):
    for i in range(1, days + 1):
        new_df['{}_day{}'.format(ticker, i)] = (new_df.shift(-i)[ticker] - new_df[ticker]) / new_df[ticker]
    clean_dataframe(new_df)


def buy_sell(*args):
    cols = [c for c in args]
    req = 0.0055
    for col in cols:
        if col > 0.01:
            return 1
        if col < -req:
            return -1
    return 0


def create_feature_and_label(tickers):
    for ticker in tickers:
        new_df['{}_target'.format(ticker)] = list(map(buy_sell,
                                                      new_df['{}_day1'.format(ticker)],
                                                      new_df['{}_day2'.format(ticker)],
                                                      new_df['{}_day3'.format(ticker)],
                                                      new_df['{}_day4'.format(ticker)],
                                                      new_df['{}_day5'.format(ticker)],
                                                      new_df['{}_day6'.format(ticker)],
                                                      new_df['{}_day7'.format(ticker)]))
    clean_dataframe(new_df)


def preprocess_data(tickers):
    combine_all_stock_data(tickers)
    for ticker in tickers:
        cal_per_change(ticker)
    create_feature_and_label(tickers)
    clean_dataframe(new_df)


def create_classifier_model_for_all_stock(tickers):
    x = new_df[[ticker for ticker in tickers]]
    x = x.pct_change()
    x.fillna(0, inplace=True)
    one = 0
    ng_one = 0
    zero = 0

    for ticker in tickers:
        y = new_df['{}_target'.format(ticker)]
        print(Counter(y.values))
        one += Counter(y.values).get(1)
        ng_one += Counter(y.values).get(-1)
        zero += Counter(y.values).get(0)
        m1 = KNeighborsClassifier()
        m2 = LogisticRegression()
        m3 = RandomForestClassifier()
        model = VotingClassifier(estimators=[('KNN', m1), ('LR', m2), ('RF', m3)])
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20)
        model.fit(x_train, y_train)
        accuracy = model.score(x_test, y_test)
        print('Accuracy for {} :: {}'.format(ticker, accuracy))
        save_model(model, ticker)

    print(one, ng_one, zero)


def save_model(model, ticker):
    path = os.path.join(os.getcwd(), 'classifier_models/{}'.format(ticker))
    fp = open(path, 'wb')
    pickle.dump(model, fp)


if __name__ == '__main__':
    new_df = pd.DataFrame()
    update_all_stock_data()
    preprocess_data(const.TICKERS)
    create_classifier_model_for_all_stock(const.TICKERS)
