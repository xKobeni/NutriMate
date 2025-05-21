from flask import Blueprint, render_template, session, redirect, url_for
from functools import wraps
from models.models import get_db_connection, get_user_preferences
from models.calorie_model import CalorieCalculator

dashboard_bp = Blueprint('dashboard', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    # Check if user has completed their profile
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_profile WHERE user_id = ?', (session['user_id'],))
    profile = cursor.fetchone()
    conn.close()
    
    if not profile:
        return redirect(url_for('profile.profile'))
    
    # Check if user has set preferences
    preferences = get_user_preferences(session['user_id'])
    if not preferences:
        return redirect(url_for('preferences.preferences'))
    
    # Calculate calorie needs
    calorie_data = CalorieCalculator.calculate_calorie_needs(
        weight=float(profile['weight']),
        height=float(profile['height']),
        age=int(profile['age']),
        gender=profile['gender'],
        activity_level=profile['activity_level']
    )
    
    return render_template('dashboard.html', 
                         email=session.get('email'), 
                         profile=profile,
                         preferences=preferences[0],
                         calorie_data=calorie_data) 