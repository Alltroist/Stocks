"""Модуль для создания БД (sqlite)
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()


class CompanyDB(Base):
    """Класс для создания схемы company
    Описание полей:
        - company_id: автоинкремент, первичный ключ
        - full_name: название компании
        - ticker: тикер (сокращенное название компании)
        - sector: сектор, в котором компания осуществляет свою дейтельность
        - summary: описание компании

    Args:
        Base ([sqlalchemy.ext.declarative.declarative_base]):
        Базовый класс для создания таблиц
    """
    __tablename__ = 'company'

    company_id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=True)
    ticker = Column(String(20), nullable=False)
    sector = Column(String(50), nullable=True)
    summary = Column(String(1000), nullable=True)

class PriceDB(Base):
    """Класс для создания схемы price
    Описание полей:
        - price_id: автоинкремент, первичный ключ
        - company_id: внешний ключ (company.company_id)
        - open_price: цена открытия
        - close_price: цена закрытия
        - high_price: наибольшая цена
        - low_price: наименьшая цена
        - volume: объем торгов
        - price_day: день торговли

    Args:
        Base ([sqlalchemy.ext.declarative.declarative_base]):
        Базовый класс для создания таблиц
    """
    __tablename__ = 'price'

    price_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('company.company_id'))
    open_price = Column(Float)
    close_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    volume = Column(Float)
    price_day = Column(Date, nullable=False)


if __name__ == "__main__":
    engine = create_engine('sqlite:///stocks.db')
    Base.metadata.create_all(engine)
