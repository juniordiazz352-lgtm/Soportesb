import discord
from config import CATEGORY_TICKETS_ID, STAFF_ROLE_ID, LOG_CHANNEL_ID
from utils.storage import load, save
from utils.embeds import ticket_embed
from views.ticket_controls import TicketControls

def create_ticket_data(user_id, channel_id, tipo):
    data = load()
    data[str(user_id)] = {
        "channel": channel_id,
        "tipo": tipo,
        "claimed": False
    }
    save(data)

def get_ticket(user_id):
    return load().get(str(user_id))

def remove_ticket(user_id):
    data = load()
    data.pop(str(user_id), None)
    save(data)

async def create_ticket(interaction, tipo):
    guild = interaction.guild
    user = interaction.user

    if get_ticket(user.id):
        return await interaction.response.send_message("❌ Ya tienes un ticket abierto.", ephemeral=True)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        guild.get_role(STAFF_ROLE_ID): discord.PermissionOverwrite(read_messages=True)
    }

    category = guild.get_channel(CATEGORY_TICKETS_ID)

    channel = await guild.create_text_channel(
        name=f"{tipo}-{user.name}",
        category=category,
        overwrites=overwrites
    )

    create_ticket_data(user.id, channel.id, tipo)

    await channel.send(embed=ticket_embed(user, tipo), view=TicketControls(user.id))

    await interaction.response.send_message(f"✅ Ticket creado: {channel.mention}", ephemeral=True)
