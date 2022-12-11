import datetime
import time
import os
import requests
import constants as const


def set_header():
    headers = {
        'User-Agent': const.USER_AGENT
    }
    return headers


class HistoricalData:

    def __init__(self, years=5):
        now = int(time.time())
        init = now - (years * 365 * 24 * 60 * 60)
        self.start = init
        self.end = now

    @property
    def start_date(self):
        return datetime.datetime.utcfromtimestamp(self.start).strftime('%a %d %b %Y')

    @property
    def end_data(self):
        return datetime.datetime.utcfromtimestamp(self.end).strftime('%a %d %b %Y')

    def get_request_data(self, interval='1d'):
        data = dict(
            period1=str(self.start),
            period2=str(self.end),
            interval=interval,
            filter='history',
            frequency=interval,
            includeAdjustedClose='true'
        )
        return data

    def get_all_data(self):
        for tick in const.TICKERS:
            print(tick)
            ticker = tick + '.NS'
            link = const.YAHOO_FINANCE_URL.format(const.YAHOO_MAIN_DOMAIN, ticker)
            res = requests.get(url=link, headers=set_header(), params=self.get_request_data(), verify=False)
            print(res)
            file_path = os.path.join(os.getcwd(), '{}/{}.csv'.format(const.HISTORICAL_DATA_BASE, tick))
            with open(file_path, 'wb') as fp:
                fp.write(res.content)

            time.sleep(1)

    def get_data(self, tick):
        print(tick)
        ticker = tick + '.NS'
        link = const.YAHOO_FINANCE_URL.format(const.YAHOO_MAIN_DOMAIN, ticker, self.start, self.end)
        res = requests.get(url=link, headers=set_header(), verify=False)
        file_path = os.path.join(os.getcwd(), '{}/{}.csv'.format(const.HISTORICAL_DATA_BASE, tick))
        with open(file_path, 'wb') as fp:
            fp.write(res.content)
