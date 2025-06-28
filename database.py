import sqlite3

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    is_active INTEGER DEFAULT 1,
                    receive_news INTEGER DEFAULT 0
                )''')
    conn.commit()
    conn.close()

def add_user(user_id: int, username: str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()

def set_receive_news(user_id: int, status: bool):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET receive_news = ? WHERE user_id = ?", (int(status), user_id))
    conn.commit()
    conn.close()

def get_active_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE receive_news = 1")
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return users
