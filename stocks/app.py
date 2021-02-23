from pathlib import Path

from flask import Flask
from flask_restful import Api

from db import db
from models.company import CompanyModel
from models.price import PriceModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(Path('data', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'alltroist'
api = Api(app)


if __name__ == '__main__':
    db.init_app(app)
    with app.test_request_context():
        db.create_all()
    app.run(port=5000, debug=True)
    
