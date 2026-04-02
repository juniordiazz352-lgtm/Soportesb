import discord

def panel_embed():
    return discord.Embed(
        title="🎫 Sistema de Tickets",
        description="Selecciona una opción del menú para abrir un ticket.",
        color=discord.Color.blurple()
    )

await channel.send(
    embed=discord.Embed(
        title=f"🎫 Ticket {tipo.upper()} #{ticket_number}",
        description=f"{user.mention} abrió un ticket.",
        color=discord.Color.green()
    ),
    view=TicketControls(user.id)
)
