from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.models import get_db_connection
import re

profile_bp = Blueprint('profile', __name__)

def validate_profile_data(data):
    errors = {}
    
    # Validate name
    if not data.get('name'):
        errors['name'] = 'Name is required'
    elif not re.match(r'^[A-Za-z\s]{2,50}$', data.get('name')):
        errors['name'] = 'Name must be 2-50 characters long and contain only letters and spaces'
    
    # Validate age
    try:
        age = int(data.get('age', 0))
        if not 1 <= age <= 120:
            errors['age'] = 'Age must be between 1 and 120'
    except ValueError:
        errors['age'] = 'Age must be a valid number'
    
    # Validate gender
    valid_genders = ['male', 'female', 'other']
    if not data.get('gender'):
        errors['gender'] = 'Gender is required'
    elif data.get('gender') not in valid_genders:
        errors['gender'] = 'Invalid gender selection'
    
    # Validate weight
    try:
        weight = float(data.get('weight', 0))
        if not 20 <= weight <= 300:
            errors['weight'] = 'Weight must be between 20 and 300 kg'
    except ValueError:
        errors['weight'] = 'Weight must be a valid number'
    
    # Validate height
    try:
        height = float(data.get('height', 0))
        if not 50 <= height <= 250:
            errors['height'] = 'Height must be between 50 and 250 cm'
    except ValueError:
        errors['height'] = 'Height must be a valid number'
    
    # Validate activity level
    valid_activity_levels = ['sedentary', 'light', 'moderate', 'very', 'extra']
    if not data.get('activity_level'):
        errors['activity_level'] = 'Activity level is required'
    elif data.get('activity_level') not in valid_activity_levels:
        errors['activity_level'] = 'Invalid activity level selection'
    
    return errors

@profile_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        # Get form data
        form_data = {
            'name': request.form.get('name'),
            'age': request.form.get('age'),
            'gender': request.form.get('gender'),
            'weight': request.form.get('weight'),
            'height': request.form.get('height'),
            'activity_level': request.form.get('activity_level')
        }
        
        # Validate form data
        errors = validate_profile_data(form_data)
        
        if errors:
            # If there are validation errors, flash them and return to form
            for field, error in errors.items():
                flash(f'{field.capitalize()}: {error}', 'danger')
            return render_template('profile.html', profile=form_data, errors=errors)
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if profile already exists
            cursor.execute('SELECT id FROM user_profile WHERE user_id = ?', (session['user_id'],))
            existing_profile = cursor.fetchone()
            
            if existing_profile:
                # Update existing profile
                cursor.execute('''
                    UPDATE user_profile 
                    SET name = ?, age = ?, gender = ?, weight = ?, height = ?, activity_level = ?
                    WHERE user_id = ?
                ''', (form_data['name'], form_data['age'], form_data['gender'], 
                      form_data['weight'], form_data['height'], form_data['activity_level'], 
                      session['user_id']))
            else:
                # Create new profile
                cursor.execute('''
                    INSERT INTO user_profile (user_id, name, age, gender, weight, height, activity_level)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (session['user_id'], form_data['name'], form_data['age'], form_data['gender'],
                      form_data['weight'], form_data['height'], form_data['activity_level']))
            
            conn.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('dashboard.dashboard'))
            
        except Exception as e:
            flash('An error occurred while saving your profile. Please try again.', 'danger')
            return render_template('profile.html', profile=form_data)
            
        finally:
            conn.close()
    
    # GET request - show the form
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_profile WHERE user_id = ?', (session['user_id'],))
    profile = cursor.fetchone()
    conn.close()
    
    return render_template('profile.html', profile=profile) 