from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from models.models import get_db_connection, create_preference, get_user_preferences
import re

preferences_bp = Blueprint('preferences', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def validate_preferences(diet_type, allergies, goal, calorie_limit):
    errors = []
    
    # Validate diet type
    valid_diets = ['regular', 'vegetarian', 'vegan', 'keto', 'paleo', 'mediterranean']
    if not diet_type or diet_type not in valid_diets:
        errors.append('Please select a valid diet type')
    
    # Validate allergies format
    if allergies:
        # Remove extra spaces and split by comma
        allergy_list = [a.strip() for a in allergies.split(',') if a.strip()]
        if len(allergy_list) > 10:
            errors.append('Maximum 10 allergies allowed')
        for allergy in allergy_list:
            if len(allergy) < 2 or len(allergy) > 30:
                errors.append('Each allergy must be between 2 and 30 characters')
            if not re.match(r'^[a-zA-Z\s-]+$', allergy):
                errors.append('Allergies can only contain letters, spaces, and hyphens')
    
    # Validate goal
    valid_goals = ['lose', 'maintain', 'gain', 'muscle']
    if not goal or goal not in valid_goals:
        errors.append('Please select a valid health goal')
    
    # Validate calorie limit
    if calorie_limit:
        try:
            calorie_limit = int(calorie_limit)
            if calorie_limit < 1000 or calorie_limit > 5000:
                errors.append('Calorie limit must be between 1000 and 5000')
        except ValueError:
            errors.append('Calorie limit must be a valid number')
    
    return errors

@preferences_bp.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    if request.method == 'POST':
        # Get form data
        diet_type = request.form.get('diet_type')
        allergies = request.form.get('allergies')
        goal = request.form.get('goal')
        calorie_limit = request.form.get('calorie_limit')
        
        # Validate inputs
        errors = validate_preferences(diet_type, allergies, goal, calorie_limit)
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('preferences.html', 
                                diet_type=diet_type,
                                allergies=allergies,
                                goal=goal,
                                calorie_limit=calorie_limit)
        
        # Create or update preferences
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if preferences exist
            cursor.execute('SELECT id FROM preference WHERE user_id = ?', (session['user_id'],))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing preferences
                cursor.execute('''
                    UPDATE preference 
                    SET diet_type = ?, allergies = ?, goal = ?, calorie_limit = ?
                    WHERE user_id = ?
                ''', (diet_type, allergies, goal, calorie_limit if calorie_limit else None, session['user_id']))
            else:
                # Create new preferences
                create_preference(
                    user_id=session['user_id'],
                    diet_type=diet_type,
                    allergies=allergies,
                    goal=goal,
                    calorie_limit=calorie_limit if calorie_limit else None
                )
            
            conn.commit()
            conn.close()
            
            flash('Preferences saved successfully!', 'success')
            return redirect(url_for('dashboard.dashboard'))
        except Exception as e:
            flash('Error saving preferences. Please try again.', 'error')
            return render_template('preferences.html')
    
    # GET request - show form
    # Get existing preferences if any
    existing_preferences = get_user_preferences(session['user_id'])
    return render_template('preferences.html', preferences=existing_preferences[0] if existing_preferences else None) 