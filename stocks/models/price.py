from db import db


class PriceModel(db.Model):
    """
    Class for creating price scheme 
    """
    __tablename__ = 'price'

    price_id = db.Column(db.Integer, primary_key=True, index=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'))
    open_price = db.Column(db.Float(precision=4))
    close_price = db.Column(db.Float(precision=4))
    high_price = db.Column(db.Float(precision=4))
    low_price = db.Column(db.Float(precision=4))
    volume = db.Column(db.Float(precision=2))
    price_day = db.Column(db.DateTime, nullable=False)

    company = db.relationship('CompanyModel')


    def __init__(self, company_id, open_price, close_price, 
        high_price, low_price, volume, price_day):
        self.company_id = company_id
        self.open_price = open_price
        self.close_price = close_price
        self.high_price = high_price
        self.low_price = low_price
        self.volume = volume
        self.price_day = price_day

    def __repr__(self):
        return f"<PriceDB({self.company_id}, {self.open_price}, " \
            f"{self.close_price}, {self.high_price}, {self.low_price}, " \
            f"{self.volume}, {self.price_day})>"