import sqlite3
import os

# Define the database file path
DB_FILE = 'fitness_tracker.db'

def connect_db():
    """Connects to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    return conn

def create_tables():
    """Creates the necessary tables if they don't exist."""
    conn = connect_db()
    cursor = conn.cursor()

    # Users table for login/signup
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    ''')

    # Exercise logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercise_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            exercise_name TEXT NOT NULL,
            sets INTEGER NOT NULL,
            reps INTEGER NOT NULL,
            calories INTEGER NOT NULL,
            log_date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database tables created or already exist.")

def add_user(username, password_hash):
    """Adds a new user to the database."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                       (username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"Error: Username '{username}' already exists.")
        return False
    finally:
        conn.close()

def get_user(username):
    """Retrieves a user's data by username."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user # Returns (id, username, password_hash) or None

def log_exercise(user_id, exercise_name, sets, reps, calories, log_date):
    """Logs an exercise entry for a given user."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO exercise_logs (user_id, exercise_name, sets, reps, calories, log_date) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, exercise_name, sets, reps, calories, log_date)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error logging exercise: {e}")
        return False
    finally:
        conn.close()

def get_exercise_logs(user_id):
    """Retrieves all exercise logs for a specific user."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT exercise_name, sets, reps, calories, log_date FROM exercise_logs WHERE user_id = ? ORDER BY log_date DESC",
        (user_id,)
    )
    logs = cursor.fetchall()
    conn.close()
    return logs # Returns a list of (exercise_name, sets, reps, calories, log_date) tuples

# Ensure tables are created when the module is imported
create_tables()
