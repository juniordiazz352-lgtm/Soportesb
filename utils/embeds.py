import discord

def panel_embed():
    return discord.Embed(
        title="🎫 Sistema de Tickets",
        description="Selecciona una opción del menú para abrir un ticket.",
        color=discord.Color.blurple()
    )

def ticket_embed(user, tipo, ticket_id):
    return discord.Embed(
        title=f"🎫 Ticket #{ticket_id}",
        description=f"{user.mention} abrió un ticket de tipo **{tipo}**.",
        color=discord.Color.green()
    )
