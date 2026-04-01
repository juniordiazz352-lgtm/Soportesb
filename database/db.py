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
