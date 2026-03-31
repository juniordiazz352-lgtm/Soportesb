import discord

def panel_embed():
    embed = discord.Embed(
        title="🎫 Sistema de Soporte",
        description="Presiona el botón para crear un ticket.",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Soporte")
    embed.timestamp = discord.utils.utcnow()
    return embed


def ticket_embed(user):
    embed = discord.Embed(
        title="🎫 Ticket creado",
        description=f"Hola {user.mention}, el staff te atenderá pronto.",
        color=discord.Color.green()
    )
    embed.set_footer(text="Soporte")
    embed.timestamp = discord.utils.utcnow()
    return embed
