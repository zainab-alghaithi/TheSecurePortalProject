import os
import shutil
import sqlite3

UPLOAD_DIR = "uploads"
DB_NAME = "portal.db"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def save_file(user_id, source_path):
    filename = os.path.basename(source_path)

    # Only allow PDFs
    if not filename.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are allowed.")

    # To avoid collisions, prefix filename with user id and underscore
    safe_filename = f"user{user_id}_{filename}"
    target_path = os.path.join(UPLOAD_DIR, safe_filename)

    shutil.copy2(source_path, target_path)

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO files (user_id, filename) VALUES (?, ?)", (user_id, safe_filename))
    conn.commit()
    conn.close()

def list_files(user_id=None, is_admin=False):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    if is_admin:
        cur.execute("SELECT users.username, files.filename FROM files JOIN users ON files.user_id = users.id")
    else:
        cur.execute("SELECT users.username, files.filename FROM files JOIN users ON files.user_id = users.id WHERE user_id = ?", (user_id,))
    files = cur.fetchall()
    conn.close()
    return files
