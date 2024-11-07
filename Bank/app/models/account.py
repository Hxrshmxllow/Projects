from app.extensions import db, bcrypt

class Account(db.Model):
    __bind_key__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    number = db.Column(db.String(20), nullable=False)
    balance = db.Column(db.Float, nullable=False)