import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# TABLAS
cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id TEXT,
    name TEXT,
    title TEXT,
    description TEXT,
    emoji TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT,
    guild_id TEXT
)
""")

conn.commit()


def add_ticket(guild_id, name, title, description, emoji):
    cursor.execute(
        "INSERT INTO tickets (guild_id, name, title, description, emoji) VALUES (?, ?, ?, ?, ?)",
        (guild_id, name, title, description, emoji)
    )
    conn.commit()


def get_tickets(guild_id):
    cursor.execute("SELECT * FROM tickets WHERE guild_id=?", (guild_id,))
    return cursor.fetchall()
