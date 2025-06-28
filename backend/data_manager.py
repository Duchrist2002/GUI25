import sqlite3

def init_db():
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
    ); 
    """)
    conn.commit()
    conn.close()

def check_login(username, email, password):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND email = ? AND password = ?", (username, email, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def add_user(username, email, password):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
