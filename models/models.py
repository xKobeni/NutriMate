import sqlite3
import os
from pathlib import Path

# Get the database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'nutrimate.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # Create instance directory if it doesn't exist
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT,
            age INTEGER,
            gender TEXT,
            weight REAL,
            height REAL,
            activity_level TEXT,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    ''')
        
    
    # Create preferences table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS preference (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            diet_type TEXT,
            allergies TEXT,
            goal TEXT,
            calorie_limit INTEGER,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    ''')


    # Meals table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS meal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        food_name TEXT NOT NULL,
        category TEXT,
        meal_type TEXT,
        calories REAL,
        protein REAL,
        carbs REAL,
        fat REAL,
        fiber REAL,
        sugar REAL,
        sodium REAL,
        cholesterol REAL
        )
    ''')

    # Create meal_log table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meal_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            meal_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            date TEXT NOT NULL,
            meal_type TEXT,
            FOREIGN KEY (user_id) REFERENCES user (id),
            FOREIGN KEY (meal_id) REFERENCES meal (id)
            )
    ''')

    # Create water_log table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS water_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            glasses INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    ''')


# Commit and close connection    
    conn.commit()
    conn.close()




def create_user(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO user (email, password) VALUES (?, ?)',
                      (email, password))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def create_preference(user_id, diet_type=None, allergies=None, goal=None, calorie_limit=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO preference (user_id, diet_type, allergies, goal, calorie_limit)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, diet_type, allergies, goal, calorie_limit))
    conn.commit()
    preference_id = cursor.lastrowid
    conn.close()
    return preference_id

def get_user_preferences(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM preference WHERE user_id = ?', (user_id,))
    preferences = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return preferences

# Note: Passwords should be hashed before calling create_user
