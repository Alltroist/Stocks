import sqlite3
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class CompanyDB(Base):
    __tablename__ = 'company'

    company_id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=True)
    ticker = Column(String(20), nullable=False)
    sector = Column(String(50), nullable=True)
    summary = Column(String(1000), nullable=True)
 
class PriceDB(Base):
    __tablename__ = 'price'

    price_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('company.company_id'))
    open_price = Column(Float)
    close_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    volume = Column(Float)
    price_day = Column(Date, nullable=False)

 


def insert_to_price(company, connection, cursor):
    query = f"""
    INSERT INTO company VALUES
        (NULL, ?, ?, ?, ?, ?, 
    )
    """

def insert_to_company(company, connection, cursor):
    query = f"""
    SELECT * FROM company
    WHERE ticker = '{company.ticker}'
    """
    result = cursor.execute(query).fetchone()
    if not result:
        query = f"""
        INSERT INTO company VALUES
            (NULL, ?, ?, ?, ?, ?)
        """
        cursor.execute(
            query, 
            (company.full_name, company.ticker, company.sector,
             company.website, company.summary
            )
        )
    connection.commit()

if __name__ == "__main__":
    engine = create_engine('sqlite:///sqlalchemy_example.db')
    Base.metadata.create_all(engine)
