import discord
import json
import os
from datetime import datetime

from utils.embeds import ticket_embed, log_embed
from view.ticket_controls import TicketControls
from system.history_system import add_history

DB_PATH = "database/counter.json"


# 🔢 CONTADOR DE TICKETS
def get_ticket_number(guild_id):
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump({}, f)

    with open(DB_PATH, "r") as f:
        data = json.load(f)

    gid = str(guild_id)

    if gid not in data:
        data[gid] = 0

    data[gid] += 1

    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)

    return data[gid]


# 🎟️ CREAR TICKET
async def create_ticket(guild: discord.Guild, user: discord.Member, tipo: str):
    try:
        # 📁 CATEGORÍA
        category = discord.utils.get(guild.categories, name="Tickets")
        if not category:
            category = await guild.create_category("Tickets")

        # 🔢 NÚMERO
        number = get_ticket_number(guild.id)

        # 🔒 PERMISOS
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True)
        }

        # 📂 CREAR CANAL
        channel = await guild.create_text_channel(
            name=f"{tipo}-{number:04d}",
            category=category,
            overwrites=overwrites,
            topic=f"Ticket de {user} | Tipo: {tipo}"
        )

        # 🎨 EMBED PRO
        embed = ticket_embed(user, tipo, number)

        await channel.send(
            content=f"👋 {user.mention}",
            embed=embed,
            view=TicketControls(user.id)
        )

        # 📊 HISTORIAL
        add_history(
            user.id,
            "ticket",
            f"Ticket creado: {channel.name}"
        )

        # 📈 LOGS PRO
        log_channel = discord.utils.get(guild.text_channels, name="ticket-logs")

        if not log_channel:
            log_channel = await guild.create_text_channel("ticket-logs")

        log = log_embed(user, tipo, channel)

        log.add_field(
            name="🕒 Fecha",
            value=f"<t:{int(datetime.utcnow().timestamp())}:F>",
            inline=False
        )

        await log_channel.send(embed=log)

    except Exception as e:
        print("❌ ERROR EN TICKET:", e)
