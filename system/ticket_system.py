import discord
import json
import os
from utils.embeds import ticket_embed, log_embed
from view.ticket_controls import TicketControls

DB_PATH = "src/database/counter.json"

def get_ticket_number(guild_id):
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump({}, f)

    with open(DB_PATH, "r") as f:
        data = json.load(f)

    guild_id = str(guild_id)

    if guild_id not in data:
        data[guild_id] = 0

    data[guild_id] += 1

    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)

    return data[guild_id]


async def create_ticket(guild, user, tipo):
    try:
        # 📁 CREAR / OBTENER CATEGORÍA
        category = discord.utils.get(guild.categories, name="Tickets")
        if not category:
            category = await guild.create_category("Tickets")

        ticket_number = get_ticket_number(guild.id)

        # 🔒 PERMISOS
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }

        channel = await guild.create_text_channel(
            name=f"{tipo}-{ticket_number:04d}",
            category=category,
            overwrites=overwrites
        )

        embed = ticket_embed(user, tipo, ticket_number)

        await channel.send(
            content=user.mention,
            embed=embed,
            view=TicketControls(user.id)
        )

        # 📊 LOGS
        log_channel = discord.utils.get(guild.text_channels, name="ticket-logs")

        if not log_channel:
            log_channel = await guild.create_text_channel("ticket-logs")

        await log_channel.send(embed=log_embed(user, tipo, channel))

    except Exception as e:
        print("❌ ERROR CREANDO TICKET:", e)
