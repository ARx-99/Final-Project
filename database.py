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

    # Exercise logs table - Added weight_kg column
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercise_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            exercise_name TEXT NOT NULL,
            sets INTEGER NOT NULL,
            reps INTEGER NOT NULL,
            weight_kg REAL, -- New column for weight in kg (can be NULL)
            calories INTEGER NOT NULL,
            log_date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Goals table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            goal_type TEXT NOT NULL, -- e.g., 'Weight Loss', 'Strength', 'Cardio'
            description TEXT NOT NULL,
            target_value REAL,
            current_value REAL,
            unit TEXT, -- e.g., 'kg', 'km', 'reps', 'sets'
            start_date TEXT NOT NULL,
            end_date TEXT,
            is_completed INTEGER DEFAULT 0, -- 0 for false, 1 for true
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

def log_exercise(user_id, exercise_name, sets, reps, weight_kg, calories, log_date):
    """Logs an exercise entry for a given user, including weight."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO exercise_logs (user_id, exercise_name, sets, reps, weight_kg, calories, log_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, exercise_name, sets, reps, weight_kg, calories, log_date)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error logging exercise: {e}")
        return False
    finally:
        conn.close()

def get_exercise_logs(user_id):
    """Retrieves all exercise logs for a specific user, including weight."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT exercise_name, sets, reps, weight_kg, calories, log_date FROM exercise_logs WHERE user_id = ? ORDER BY log_date DESC",
        (user_id,)
    )
    logs = cursor.fetchall()
    conn.close()
    return logs # Returns a list of (exercise_name, sets, reps, weight_kg, calories, log_date) tuples

def add_goal(user_id, goal_type, description, target_value, current_value, unit, start_date, end_date=None, is_completed=0):
    """Adds a new fitness goal for a user."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO goals (user_id, goal_type, description, target_value, current_value, unit, start_date, end_date, is_completed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, goal_type, description, target_value, current_value, unit, start_date, end_date, is_completed)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding goal: {e}")
        return False
    finally:
        conn.close()

def get_goals(user_id, include_completed=False):
    """Retrieves goals for a specific user."""
    conn = connect_db()
    cursor = conn.cursor()
    if include_completed:
        cursor.execute("SELECT id, goal_type, description, target_value, current_value, unit, start_date, end_date, is_completed FROM goals WHERE user_id = ? ORDER BY is_completed ASC, end_date ASC", (user_id,))
    else:
        cursor.execute("SELECT id, goal_type, description, target_value, current_value, unit, start_date, end_date, is_completed FROM goals WHERE user_id = ? AND is_completed = 0 ORDER BY end_date ASC", (user_id,))
    goals = cursor.fetchall()
    conn.close()
    return goals

def update_goal_progress(goal_id, new_current_value, is_completed=None):
    """Updates the current progress of a goal."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        if is_completed is not None:
            cursor.execute("UPDATE goals SET current_value = ?, is_completed = ? WHERE id = ?", (new_current_value, is_completed, goal_id))
        else:
            cursor.execute("UPDATE goals SET current_value = ? WHERE id = ?", (new_current_value, goal_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating goal: {e}")
        return False
    finally:
        conn.close()

def delete_goal(goal_id):
    """Deletes a goal by its ID."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting goal: {e}")
        return False
    finally:
        conn.close()


# Ensure tables are created when the module is imported
create_tables()
