import requests
import json 
import sqlite3
from collections import namedtuple

from tqdm import tqdm

from init_db import insert_to_db

Price = namedtuple("Price", 
    [
        "ticker", "open", "close",
        "high", "low", "volume", "price_day"
    ]
)


class Company:
    def __init__(self, ticker):
        self.ticker = ticker
        self.full_name = None
        self.website = None
        self.sector = None
        self.summary = None
        self.price = None
        self.get_short_name()
        self.get_company_info()
        self.get_price()

    def __str__(self):
        return f"company {ticker}"

    def get_short_name(self):
        result = requests.get(
            f"https://query1.finance.yahoo.com/v10/finance/" \
            f"quoteSummary/{self.ticker}?modules=price"
        ).json()
        self.error = result['quoteSummary']['error'] != None
        if not self.error:
            self.full_name = result['quoteSummary']['result'][0]['price']['shortName']

    def get_company_info(self):
        if not self.error:
            result = requests.get(
                f"https://query1.finance.yahoo.com/v10/finance/" \
                f"quoteSummary/{self.ticker}?modules=assetProfile"
            ).json()
            if result['quoteSummary']['error'] == None:
                profile = result['quoteSummary']['result'][0]['assetProfile']
                self.website = profile.get('website') 
                self.sector = profile.get('sector')
                self.summary = profile.get('longBusinessSummary')
            #self.founder = result['quoteSummary']['result'][0]['assetProfile']['companyOfficers']

    def get_price(self, start=0, end=9999999999, interval="1d"):
        if not self.error:
            result = requests.get(
                f"https://query1.finance.yahoo.com/v8/finance/" \
                f"chart/?symbol={self.ticker}&period1={start}&" \
                f"period2={end}&interval={interval}&includePrePost=true"
            ).json()
            if ((result['chart']['error'] == None) 
                and ('open' in result['chart']['result'][0]['indicators']['quote'][0])):
                self.price = [Price(
                        self.ticker,
                        open_price,
                        close_price,
                        high_price,
                        low_price,
                        volume_price,
                        day 
                    )
                    for open_price, close_price, high_price, low_price, volume_price, day 
                    in zip(
                        result['chart']['result'][0]['indicators']['quote'][0]['open'],
                        result['chart']['result'][0]['indicators']['quote'][0]['close'],
                        result['chart']['result'][0]['indicators']['quote'][0]['high'],
                        result['chart']['result'][0]['indicators']['quote'][0]['low'],
                        result['chart']['result'][0]['indicators']['quote'][0]['volume'],
                        result['chart']['result'][0]['timestamp']
                    )
                ]



if __name__ == "__main__":
    with open("stocks.json", "r") as f:
        company_list = json.load(f)

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    for element in company_list[:10]:
        company = Company(element)
        print(element, company.price)
    
    #for element in tqdm(company_list):
    #    company = Company(element)
    #    insert_to_db(company, connection, cursor)

    connection.close()