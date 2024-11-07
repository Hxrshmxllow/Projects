from app.extensions import db, bcrypt

class Transaction(db.Model):
    __bind_key__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)