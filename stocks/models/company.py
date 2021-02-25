from db import db


class CompanyModel(db.Model):
    """
    Class for creating company scheme
    """
    __tablename__ = 'company'

    company_id = db.Column(db.Integer, primary_key=True, index=True)
    full_name = db.Column(db.String(100), nullable=True)
    ticker = db.Column(db.String(20), nullable=False)
    sector = db.Column(db.String(50), nullable=True)
    summary = db.Column(db.String(1000), nullable=True)

    price = db.relationship('PriceModel', lazy='dynamic')

    def __init__(self, full_name, ticker, sector, summary):
        self.full_name = full_name
        self.ticker = ticker
        self.sector = sector
        self.summary = summary 

    def __repr__(self):
        return f"<CompanyModel({self.full_name}, {self.ticker}, " \
            f"{self.sector}, {self.summary})>"

    