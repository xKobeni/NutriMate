import sqlite3
import os

# Get the database path
DB_PATH = os.path.join('instance', 'nutrimate.db')

def check_tables():
    try:
        # Connect to the database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get list of all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("\nTables in the database:")
        print("-" * 20)
        for table in tables:
            print(f"Table: {table[0]}")
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table[0]})")
            columns = cursor.fetchall()
            print("Columns:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            print("-" * 20)
        
        conn.close()
        
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
        print("Database might not exist yet. Make sure you've run the application at least once.")

if __name__ == "__main__":
    check_tables() 