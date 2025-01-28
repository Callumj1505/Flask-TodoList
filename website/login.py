from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Auth
from . import db


auth = Blueprint("auth", __name__)


@auth.route('/Sign-Up', methods=['POST', 'GET'])
def Signup_Home():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        
        if len(password) < 3:
            flash('Password must be longer than 3 Characters.', 'error')
            return render_template('signup.html')
        
        if len(email) < 5 or "@" not in email:
            flash('Email Must be Longer than 5 Charcters. Or email doesnt contain "@"', 'error')
            return render_template('signup.html')
        
        if password2 != password:
            flash('Passwords need to match.', 'error')
            return render_template('signup.html')
            
        exsisting_user = Auth.query.filter_by(email=email).first()
        if exsisting_user:
            flash('This email already exsists. Please eneter another email.', 'error')
            return render_template('signup.html')
        
        hashed_password = generate_password_hash(password, method ='pbkdf2:sha256')
        
        new_user = Auth(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account has been created successfully. Please login.', 'success')
        return redirect(url_for('auth.login_Home'))
    
    return render_template('signup.html')

























@auth.route('/Login', methods = ['GET', 'POST'] )
def login_Home():
    if request.method == 'POST':
        email = request.form.get("emaillogin")
        password = request.form.get("passwordlogin")
        
        user = Auth.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('auth.login_Home'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html')
        
@auth.route('/logout')
def Logout():
    session.pop('user_id', None)
    flash('you have been logged out successfully!', 'success')
    return redirect(url_for('auth.login_Home'))