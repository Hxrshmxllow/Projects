from flask import Flask
from .config import Config
from .extensions import db, bcrypt, jwt, cors
from .routes import auth_bp

def createApp():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    app.register_blueprint(auth_bp)
    
    with app.app_context():
        from .models import user, account, transaction
        db.create_all(bind_key='users')
        db.create_all(bind_key='accounts')
        db.create_all(bind_key='transactions')
    
    return app