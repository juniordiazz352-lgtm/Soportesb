import json
import os
from datetime import datetime

DB = "database/history.json"

def load():
    if not os.path.exists(DB):
        with open(DB, "w") as f:
            json.dump({}, f)

    with open(DB, "r") as f:
        return json.load(f)

def save(data):
    with open(DB, "w") as f:
        json.dump(data, f, indent=4)

def add_history(user_id, tipo, content):
    data = load()
    uid = str(user_id)

    if uid not in data:
        data[uid] = []

    data[uid].append({
        "tipo": tipo,
        "contenido": content,
        "fecha": datetime.utcnow().isoformat()
    })

    save(data)

def get_history(user_id):
    return load().get(str(user_id), [])
