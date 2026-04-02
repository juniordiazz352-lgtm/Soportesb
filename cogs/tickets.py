import discord
from discord.ext import commands
from discord import app_commands
from database.db import add_ticket, get_tickets, set_ticket_log, get_ticket_log
import config
import html
import os

# =========================
# 🔒 CERRAR + TRANSCRIPT HTML
# =========================
class CloseView(discord.ui.View):
    def __init__(self, ticket_name):
        super().__init__(timeout=None)
        self.ticket_name = ticket_name

    @discord.ui.button(label="Confirmar cierre", style=discord.ButtonStyle.red)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):

        channel = interaction.channel
        guild = interaction.guild

        mensajes_html = ""

        async for msg in channel.history(limit=None, oldest_first=True):

            author = html.escape(str(msg.author))
            content = html.escape(msg.content)
            time = msg.created_at.strftime("%d/%m/%Y %H:%M")
            avatar = msg.author.display_avatar.url

            mensajes_html += f"""
            <div class="msg">
                <img src="{avatar}" class="avatar">
                <div>
                    <div class="header">
                        <span class="user">{author}</span>
                        <span class="time">{time}</span>
                    </div>
                    <div class="content">{content}</div>
                </div>
            </div>
            """

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body {{
    background: #0f172a;
    color: white;
    font-family: Arial;
    padding: 20px;
}}
.msg {{
    display: flex;
    gap: 10px;
    margin-bottom: 15px;
}}
.avatar {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
}}
.user {{
    font-weight: bold;
}}
.time {{
    color: gray;
    font-size: 12px;
    margin-left: 10px;
}}
.content {{
    margin-top: 3px;
}}
</style>
</head>
<body>
<h2>Transcript - {channel.name}</h2>
{mensajes_html}
</body>
</html>
"""

        # 📂 GUARDAR EN WEB
        os.makedirs("web/transcripts", exist_ok=True)
        file_path = f"web/transcripts/{channel.id}.html"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        file = discord.File(file_path, filename=f"{channel.name}.html")

        # 📡 ENVIAR A LOGS
        log_id = get_ticket_log(str(guild.id), self.ticket_name)
        if log_id:
            log_channel = guild.get_channel(int(log_id))
            if log_channel:
                await log_channel.send(
                    content=f"📁 Transcript {channel.name}",
                    file=file
                )

        await interaction.response.send_message("🔒 Ticket cerrado", ephemeral=True)
        await channel.delete()


# =========================
# 🎫 BOTONES TICKET
# =========================
class TicketView(discord.ui.View):
    def __init__(self, ticket_name):
        super().__init__(timeout=None)
        self.ticket_name = ticket_name

    @discord.ui.button(label="🔒 Cerrar Ticket", style=discord.ButtonStyle.red)
    async def cerrar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "¿Seguro que quieres cerrar?",
            view=CloseView(self.ticket_name),
            ephemeral=True
        )


# =========================
# 🤖 COG PRINCIPAL
# =========================
class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_owner(self, i):
        return i.user.id == config.OWNER_ID

    # 🔥 CREAR TICKET + LOG
    @app_commands.command(name="crear_ticket")
    async def crear_ticket(
        self,
        i: discord.Interaction,
        nombre: str,
        titulo: str,
        descripcion: str,
        canal_logs: discord.TextChannel
    ):
        if not self.is_owner(i):
            return await i.response.send_message("❌ Solo owner", ephemeral=True)

        add_ticket(str(i.guild.id), nombre, titulo, descripcion)
        set_ticket_log(str(i.guild.id), nombre, str(canal_logs.id))

        await i.response.send_message("✅ Ticket creado con logs")

    # 🎛️ PANEL
    @app_commands.command(name="panel_ticket")
    async def panel(self, i: discord.Interaction):

        tickets = get_tickets(str(i.guild.id))

        if not tickets:
            return await i.response.send_message("❌ No hay tickets", ephemeral=True)

        options = [
            discord.SelectOption(label=t[0], description=t[2])
            for t in tickets
        ]

        class Menu(discord.ui.Select):
            def __init__(self):
                super().__init__(placeholder="Selecciona ticket", options=options)

            async def callback(self, interaction: discord.Interaction):
                guild = interaction.guild
                ticket_name = self.values[0]

                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    interaction.user: discord.PermissionOverwrite(read_messages=True)
                }

                channel = await guild.create_text_channel(
                    name=f"ticket-{interaction.user.name}",
                    overwrites=overwrites
                )

                embed = discord.Embed(
                    title="🎫 Ticket abierto",
                    description=f"Tipo: {ticket_name}",
                    color=discord.Color.green()
                )

                await channel.send(
                    content=interaction.user.mention,
                    embed=embed,
                    view=TicketView(ticket_name)
                )

                await interaction.response.send_message(
                    f"✅ Ticket creado: {channel.mention}",
                    ephemeral=True
                )

        view = discord.ui.View()
        view.add_item(Menu())

        await i.channel.send("🎫 Panel de tickets", view=view)
        await i.response.send_message("✅ Panel enviado", ephemeral=True)


class TicketView(discord.ui.View):
    def __init__(self, ticket_name):
        super().__init__(timeout=None)
        self.ticket_name = ticket_name
        self.claimed = None

    @discord.ui.button(label="📌 Reclamar", style=discord.ButtonStyle.blurple)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        from database.db import get_staff_roles

        if not is_staff(interaction.user, interaction.guild):
            return await interaction.response.send_message("❌ No eres staff", ephemeral=True)

        self.claimed = interaction.user

        await interaction.channel.send(f"📌 Ticket reclamado por {interaction.user.mention}")
        await interaction.response.defer()

    @discord.ui.button(label="➕ Añadir", style=discord.ButtonStyle.gray)
    async def add(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not is_staff(interaction.user, interaction.guild):
            return await interaction.response.send_message("❌ No staff", ephemeral=True)

        await interaction.response.send_message("Menciona usuario o rol")

        msg = await interaction.client.wait_for(
            "message",
            check=lambda m: m.author == interaction.user
        )

        for user in msg.mentions:
            await interaction.channel.set_permissions(user, read_messages=True)

        for role in msg.role_mentions:
            await interaction.channel.set_permissions(role, read_messages=True)

        await interaction.channel.send("✅ Añadido")

        


async def setup(bot):
    await bot.add_cog(Tickets(bot))
