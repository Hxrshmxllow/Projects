from flask import Blueprint, request, jsonify, redirect, url_for, render_template
import sys
from .models.user import User
from .models.account import Account
from .models.transaction import Transaction
from .extensions import db, bcrypt, jwt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/')
def index():
    return redirect(url_for('auth_bp.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        print(user)
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        return jsonify({'msg': "Bad username or password"}), 401
    else:
        return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if User.query.filter_by(username=username).first():
            return jsonify("Username already exists"), 409
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@auth_bp.route('/settings')
def settings():
    return render_template('settings.html')

@auth_bp.route('/fund-transfer')
def fundTransfer():
    return render_template('fund-transfer.html')

@auth_bp.route('/accounts')
def accounts():
    return render_template('accounts.html')

@auth_bp.route('/my-cards')
def myCards():
    return render_template('cards.html')

