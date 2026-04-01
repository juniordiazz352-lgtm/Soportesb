import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# TABLAS
cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id TEXT,
    nombre TEXT,
    titulo TEXT,
    descripcion TEXT
)
""")

conn.commit()

def add_ticket(guild_id, nombre, titulo, descripcion):
    cursor.execute(
        "INSERT INTO tickets (guild_id, nombre, titulo, descripcion) VALUES (?, ?, ?, ?)",
        (guild_id, nombre, titulo, descripcion)
    )
    conn.commit()

def get_tickets(guild_id):
    cursor.execute("SELECT nombre, titulo, descripcion FROM tickets WHERE guild_id=?", (guild_id,))
    return cursor.fetchall()

# LOGS
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    guild_id TEXT,
    log_channel TEXT
)
""")

def set_logs(guild_id, channel_id):
    cursor.execute("DELETE FROM logs WHERE guild_id=?", (guild_id,))
    cursor.execute(
        "INSERT INTO logs (guild_id, log_channel) VALUES (?, ?)",
        (guild_id, channel_id)
    )
    conn.commit()

def get_logs(guild_id):
    cursor.execute("SELECT log_channel FROM logs WHERE guild_id=?", (guild_id,))
    result = cursor.fetchone()
    return result[0] if result else None
