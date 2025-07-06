import sqlite3
from bcrypt import hashpw, gensalt, checkpw

DB_NAME = "portal.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Create users table
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('admin', 'user')) NOT NULL DEFAULT 'user'
    )''')

    # Create files table
    cur.execute('''CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        filename TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

    conn.commit()
    conn.close()

def register_user(username, password, role="user"):
    from utils import is_strong_password

    if not is_strong_password(password):
        return "weak"

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    hashed_pw = hashpw(password.encode(), gensalt())

    try:
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (username, hashed_pw, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, username, password, role FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if row and checkpw(password.encode(), row[2]):
        return {"id": row[0], "username": row[1], "role": row[3]}
    return None
