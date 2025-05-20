from flask import Blueprint, render_template, request, redirect, url_for, session
from models.models import get_user_by_email, create_user
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user_by_email(email)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['email'] = user['email']
            return redirect(url_for('dashboard.dashboard'))
        else:
            error = 'Invalid email or password.'
    return render_template('login.html', error=error)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            error = 'Passwords do not match.'
        else:
            hashed_password = generate_password_hash(password)
            user_id = create_user(email, hashed_password)
            if user_id:
                return redirect(url_for('auth.login'))
            else:
                error = 'Email is already registered.'
    return render_template('register.html', error=error)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login')) 