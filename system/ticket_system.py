import discord
from database.db import load, save
from utils.embeds import ticket_embed
from view.ticket_controls import TicketControls

TICKETS_FILE = "database/tickets.json"
GUILDS_FILE = "database/guilds.json"
COUNTER_FILE = "database/counter.json"

COUNTER_FILE = "database/counter.json"

def get_next_ticket_number(tipo):
    data = load(COUNTER_FILE)

    if tipo not in data:
        data[tipo] = 0

    data[tipo] += 1
    save(COUNTER_FILE, data)

    return str(data[tipo]).zfill(4)

  

def save_ticket(user_id, guild_id, channel_id, tipo):
    data = load(TICKETS_FILE)
    data[str(user_id)] = {
        "guild": guild_id,
        "channel": channel_id,
        "tipo": tipo
    }
    save(TICKETS_FILE, data)

def has_ticket(user_id):
    return str(user_id) in load(TICKETS_FILE)

def remove_ticket(user_id):
    data = load(TICKETS_FILE)
    data.pop(str(user_id), None)
    save(TICKETS_FILE, data)

async def create_ticket(interaction, tipo):
    guild = interaction.guild
    user = interaction.user

    if has_ticket(user.id):
        return await interaction.response.send_message("❌ Ya tienes ticket.", ephemeral=True)

    config = get_guild_config(guild.id)
    if not config:
        return await interaction.response.send_message("❌ Servidor no configurado.", ephemeral=True)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        user: discord.PermissionOverwrite(read_messages=True),
        guild.get_role(config["staff_role"]): discord.PermissionOverwrite(read_messages=True)
    }

    category = guild.get_channel(config["category"])

ticket_number = get_next_ticket_number(tipo.lower())

import discord

async def create_ticket(guild, user, tipo):
    category = discord.utils.get(guild.categories, name="Tickets")

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        user: discord.PermissionOverwrite(read_messages=True)
    }

    channel = await guild.create_text_channel(
        name=f"{tipo}-{user.name}",
        category=category,
        overwrites=overwrites
    )

    await channel.send(f"{user.mention} ✅ ticket creado")
