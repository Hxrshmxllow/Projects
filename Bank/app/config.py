import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_BINDS = {
        'users': 'sqlite:///users.db',
        'accounts': 'sqlite:///accounts.db'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'lanLJej3K7'