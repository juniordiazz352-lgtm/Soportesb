import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# 🎫 TICKETS (TIPOS)
cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id TEXT,
    nombre TEXT,
    titulo TEXT,
    descripcion TEXT
)
""")

# 📡 LOGS POR PANEL
cursor.execute("""
CREATE TABLE IF NOT EXISTS ticket_logs (
    guild_id TEXT,
    nombre TEXT,
    log_channel TEXT
)
""")

conn.commit()

# =========================
# 🎫 TICKETS
# =========================
def add_ticket(guild_id, nombre, titulo, descripcion):
    cursor.execute(
        "INSERT INTO tickets (guild_id, nombre, titulo, descripcion) VALUES (?, ?, ?, ?)",
        (guild_id, nombre, titulo, descripcion)
    )
    conn.commit()

def get_tickets(guild_id):
    cursor.execute(
        "SELECT nombre, titulo, descripcion FROM tickets WHERE guild_id=?",
        (guild_id,)
    )
    return cursor.fetchall()

# =========================
# 📡 LOGS POR PANEL
# =========================
def set_ticket_log(guild_id, nombre, channel_id):
    cursor.execute(
        "DELETE FROM ticket_logs WHERE guild_id=? AND nombre=?",
        (guild_id, nombre)
    )
    cursor.execute(
        "INSERT INTO ticket_logs VALUES (?, ?, ?)",
        (guild_id, nombre, channel_id)
    )
    conn.commit()

def get_ticket_log(guild_id, nombre):
    cursor.execute(
        "SELECT log_channel FROM ticket_logs WHERE guild_id=? AND nombre=?",
        (guild_id, nombre)
    )
    r = cursor.fetchone()
    return r[0] if r else None
