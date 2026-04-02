import discord
from datetime import datetime

# 🎫 EMBED PRINCIPAL DEL TICKET
def ticket_embed(user, tipo, ticket_number):
    embed = discord.Embed(
        title=f"🎫 Ticket #{ticket_number:04d}",
        description=(
            f"👤 **Usuario:** {user.mention}\n"
            f"📂 **Tipo:** {tipo}\n"
            f"🕒 **Creado:** <t:{int(datetime.utcnow().timestamp())}:F>"
        ),
        color=discord.Color.green()
    )

    embed.set_thumbnail(url=user.display_avatar.url)

    embed.add_field(
        name="📌 Estado",
        value="🟢 Abierto",
        inline=True
    )

    embed.add_field(
        name="👨‍💼 Soporte",
        value="⏳ Esperando staff...",
        inline=True
    )

    embed.set_footer(
        text=f"ID Usuario: {user.id}",
        icon_url=user.display_avatar.url
    )

    return embed


# 🔒 EMBED CUANDO SE CIERRA EL TICKET
def closed_ticket_embed(user, closed_by):
    embed = discord.Embed(
        title="🔒 Ticket Cerrado",
        description=(
            f"👤 **Usuario:** {user.mention}\n"
            f"🔧 **Cerrado por:** {closed_by.mention}\n"
            f"🕒 **Fecha:** <t:{int(datetime.utcnow().timestamp())}:F>"
        ),
        color=discord.Color.red()
    )

    embed.set_thumbnail(url=user.display_avatar.url)

    return embed


# 📋 EMBED DE PANEL DE TICKETS
def panel_embed():
    embed = discord.Embed(
        title="🎟️ Sistema de Tickets",
        description=(
            "Selecciona una opción para crear un ticket:\n\n"
            "🛠️ **Soporte**\n"
            "💰 **Compras**\n"
            "📩 **Reportes**"
        ),
        color=discord.Color.blurple()
    )

    embed.set_footer(text="Sistema de soporte automático")

    return embed


# 📝 EMBED DE FORMULARIOS
def form_embed(user, form_name, responses):
    embed = discord.Embed(
        title=f"📋 Formulario: {form_name}",
        description=f"👤 Enviado por: {user.mention}",
        color=discord.Color.orange()
    )

    embed.set_thumbnail(url=user.display_avatar.url)

    for pregunta, respuesta in responses.items():
        embed.add_field(
            name=f"❓ {pregunta}",
            value=respuesta or "Sin respuesta",
            inline=False
        )

    embed.set_footer(text=f"ID Usuario: {user.id}")

    return embed


# 📜 EMBED DE LOG (TIPO TICKET KING)
def log_embed(title, description, user):
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.dark_gold()
    )

    embed.set_author(
        name=str(user),
        icon_url=user.display_avatar.url
    )

    embed.timestamp = datetime.utcnow()

    return embed
