import discord

def panel_embed():
    return discord.Embed(
        title="🎫 Sistema de Tickets",
        description="Selecciona una opción del menú para abrir un ticket.",
        color=discord.Color.blurple()
    )

def ticket_embed(user, tipo):
    return discord.Embed(
        title=f"🎫 Ticket - {tipo}",
        description=f"{user.mention} ha abierto un ticket.\nUn staff te atenderá pronto.",
        color=discord.Color.green()
    )
