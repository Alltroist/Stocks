"""
Main module for updating DB:
    Load new company / update old company
    Load new price 
"""
import requests
import json
from collections import namedtuple
from pathlib import Path
from time import time
from datetime import datetime

from tqdm import tqdm

from models.company import CompanyModel
from models.price import PriceModel



Price = namedtuple("Price", 
    [
        "open_price", "close_price", "high_price", 
        "low_price", "volume", "price_day"
    ]
)


class Company:
    """
    Main class for storing information about company:
        - name
        - additional info (like sector, website etc.)
        - price (per day)
    """
    def __init__(self, ticker):
        self.ticker = ticker
        self.full_name = None
        self.website = None
        self.sector = None
        self.summary = None
        self.price = None
        self.company_id = None
        self.__get_short_name()
        self.__get_company_info()
        self.__get_price(end=int(time()))

    def __str__(self):
        return f"<Company(name={self.full_name}, ticker={self.ticker}," \
            f"website={self.website}, sector={self.sector}, summary={self.summary})>" 

    def __repr__(self):
        return f"<Company({self.ticker})>"

    def __get_short_name(self):
        result = requests.get(
            f"https://query1.finance.yahoo.com/v10/finance/" \
            f"quoteSummary/{self.ticker}?modules=price"
        ).json()
        self.error = result['quoteSummary']['error'] is not None
        if not self.error:
            self.full_name = result['quoteSummary']['result'][0]['price']['shortName']

    def __get_company_info(self):
        if not self.error:
            result = requests.get(
                f"https://query1.finance.yahoo.com/v10/finance/" \
                f"quoteSummary/{self.ticker}?modules=assetProfile"
            ).json()
            if result['quoteSummary']['error'] is None:
                profile = result['quoteSummary']['result'][0]['assetProfile']
                self.website = profile.get('website') 
                self.sector = profile.get('sector')
                self.summary = profile.get('longBusinessSummary')
            #self.founder = result['quoteSummary']['result'][0]['assetProfile']['companyOfficers']

    def __get_price(self, start=1612126800, end=9999999999, interval="1d"):
        if not self.error:
            result = requests.get(
                f"https://query1.finance.yahoo.com/v8/finance/" \
                f"chart/?symbol={self.ticker}&period1={start}&" \
                f"period2={end}&interval={interval}&includePrePost=true"
            ).json()
            if ((result['chart']['error'] == None) 
                and ('open' in result['chart']['result'][0]['indicators']['quote'][0])):
                self.price = [Price(
                        open_price,
                        close_price,
                        high_price,
                        low_price,
                        volume,
                        datetime.utcfromtimestamp(day)
                    )
                    for open_price, close_price, high_price, low_price, volume, day 
                    in zip(
                        result['chart']['result'][0]['indicators']['quote'][0]['open'],
                        result['chart']['result'][0]['indicators']['quote'][0]['close'],
                        result['chart']['result'][0]['indicators']['quote'][0]['high'],
                        result['chart']['result'][0]['indicators']['quote'][0]['low'],
                        result['chart']['result'][0]['indicators']['quote'][0]['volume'],
                        result['chart']['result'][0]['timestamp']
                    )
                ]

    def insert_company(self, session):
        company = CompanyModel(self.full_name, self.ticker, self.sector, self.summary)
        session.add(company)
        session.flush()
        self.company_id = company.company_id

    def insert_price(self, session):
        if self.price is not None:
            session.add_all([PriceDB(company_id=self.company_id, **price._asdict()) 
                for price in self.price])



if __name__ == "__main__":
    with open(Path("static", "data", "company_list.json") , "r") as f:
        company_list = json.load(f)

    engine = create_engine('sqlite:///' + str(Path("static", "data", "company_stocks.db")))
    DBSession = sessionmaker(bind=engine, autocommit=True)
    session = DBSession()
    
    for element in tqdm(company_list):
        company = Company(element)
        company.insert_company(session)
        company.insert_price(session)

    
    #for element in tqdm(company_list):
    #    company = Company(element)
    #    insert_to_db(company, connection, cursor)

    #connection.close()