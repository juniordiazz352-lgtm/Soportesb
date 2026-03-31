import discord
from discord.ext import commands, tasks
from discord import app_commands
import time

from utils.storage import load_data, save_data
from utils.checks import is_owner
from utils.transcript import create_transcript

FILE = "data/tickets.json"
STATS = "data/stats.json"


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auto_close.start()

    # 👮 AGREGAR ROL STAFF
    @app_commands.command(name="agregar_rol_staff")
    async def agregar_staff(self, interaction: discord.Interaction, rol: discord.Role):

        if not is_owner(interaction.user):
            return await interaction.response.send_message("❌ Solo dueño", ephemeral=True)

        data = load_data(FILE)

        if rol.id in data["staff_roles"]:
            return await interaction.response.send_message("⚠️ Ya es staff", ephemeral=True)

        data["staff_roles"].append(rol.id)
        save_data(FILE, data)

        await interaction.response.send_message(f"✅ {rol.name} agregado como staff")

    # 🔔 CONFIGURAR LOGS
    @app_commands.command(name="set_logs")
    async def set_logs(self, interaction: discord.Interaction, canal: discord.TextChannel):

        if not is_owner(interaction.user):
            return await interaction.response.send_message("❌ Solo dueño", ephemeral=True)

        data = load_data(FILE)
        data["log_channel"] = canal.id
        save_data(FILE, data)

        await interaction.response.send_message("✅ Canal de logs configurado")

    # 🎫 CREAR TIPO DE TICKET
    @app_commands.command(name="crear_ticket")
    async def crear_ticket(
        self,
        interaction: discord.Interaction,
        nombre: str,
        titulo: str,
        descripcion: str,
        emoji: str
    ):
        if not is_owner(interaction.user):
            return await interaction.response.send_message("❌ Solo dueño", ephemeral=True)

        data = load_data(FILE)

        data["tickets"][nombre] = {
            "titulo": titulo,
            "descripcion": descripcion,
            "emoji": emoji
        }

        save_data(FILE, data)

        await interaction.response.send_message("✅ Ticket creado PRO MAX", ephemeral=True)

    # 🎛️ PANEL TIPO APPY (SELECT MENU)
    @app_commands.command(name="panel_ticket")
    async def panel_ticket(
        self,
        interaction: discord.Interaction,
        canal: discord.TextChannel,
        categoria: discord.CategoryChannel,
        titulo: str,
        descripcion: str
    ):
        if not is_owner(interaction.user):
            return await interaction.response.send_message("❌ Solo dueño", ephemeral=True)

        data = load_data(FILE)

        if not data["tickets"]:
            return await interaction.response.send_message("❌ No hay tickets creados", ephemeral=True)

        options = [
            discord.SelectOption(
                label=info["titulo"],
                description=info["descripcion"][:100],
                emoji=info["emoji"],
                value=nombre
            )
            for nombre, info in data["tickets"].items()
        ]

        class TicketSelect(discord.ui.Select):
            def __init__(self):
                super().__init__(
                    placeholder="🎫 Selecciona un tipo de ticket",
                    options=options
                )

            async def callback(self, inter: discord.Interaction):

                guild = inter.guild
                user = inter.user
                data = load_data(FILE)

                # ❌ Anti duplicados
                for ch in guild.text_channels:
                    if ch.name == f"ticket-{user.id}":
                        return await inter.response.send_message("❌ Ya tienes un ticket", ephemeral=True)

                ticket_info = data["tickets"][self.values[0]]

                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    user: discord.PermissionOverwrite(view_channel=True, send_messages=True)
                }

                # 👮 Staff
                for role_id in data["staff_roles"]:
                    role = guild.get_role(role_id)
                    if role:
                        overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

                channel = await guild.create_text_channel(
                    name=f"ticket-{user.id}",
                    category=categoria,
                    overwrites=overwrites
                )

                embed = discord.Embed(
                    title=ticket_info["titulo"],
                    description=ticket_info["descripcion"],
                    color=discord.Color.blurple()
                )

                await channel.send(
                    content=f"🎫 {user.mention}",
                    embed=embed,
                    view=TicketButtons(user.id)
                )

                await inter.response.send_message("✅ Ticket creado", ephemeral=True)

        class PanelView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)
                self.add_item(TicketSelect())

        embed = discord.Embed(
            title=titulo,
            description=descripcion,
            color=discord.Color.blurple()
        )

        await canal.send(embed=embed, view=PanelView())
        await interaction.response.send_message("✅ Panel creado tipo Appy", ephemeral=True)

    # ⏱️ AUTO CLOSE
    @tasks.loop(minutes=5)
    async def auto_close(self):
        await self.bot.wait_until_ready()
        now = time.time()

        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if "ticket-" in channel.name:
                    try:
                        last_msg = [m async for m in channel.history(limit=1)][0]
                        if now - last_msg.created_at.timestamp() > 3600:
                            await channel.send("⏱️ Cerrado por inactividad")
                            await channel.delete()
                    except:
                        pass


# 🔘 BOTONES
class TicketButtons(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id
        self.claimed = None

    def is_staff(self, interaction):
        data = load_data(FILE)
        return any(role.id in data["staff_roles"] for role in interaction.user.roles)

    @discord.ui.button(label="Reclamar", emoji="👤", style=discord.ButtonStyle.primary)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not self.is_staff(interaction):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        self.claimed = interaction.user

        stats = load_data(STATS)
        stats[str(interaction.user.id)] = stats.get(str(interaction.user.id), 0) + 1
        save_data(STATS, stats)

        await interaction.response.send_message(f"👤 Ticket reclamado por {interaction.user.mention}")

    @discord.ui.button(label="Cerrar", emoji="🔒", style=discord.ButtonStyle.danger)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not self.is_staff(interaction):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        data = load_data(FILE)

        file = await create_transcript(interaction.channel)

        log_channel = interaction.guild.get_channel(data["log_channel"])

        if log_channel:
            await log_channel.send(
                f"📁 Ticket cerrado por {interaction.user.mention}",
                file=discord.File(file)
            )

        await interaction.channel.delete()

    @discord.ui.button(label="Añadir", emoji="➕", style=discord.ButtonStyle.secondary)
    async def add(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not self.is_staff(interaction):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        await interaction.response.send_message("Menciona usuario o rol", ephemeral=True)

        def check(m): return m.author == interaction.user
        msg = await interaction.client.wait_for("message", check=check)

        for user in msg.mentions:
            await interaction.channel.set_permissions(user, view_channel=True)

        for role in msg.role_mentions:
            await interaction.channel.set_permissions(role, view_channel=True)

        await interaction.followup.send("✅ Añadido")

    @discord.ui.button(label="Reabrir", emoji="🔓", style=discord.ButtonStyle.success)
    async def reopen(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not self.is_staff(interaction):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        await interaction.channel.set_permissions(
            interaction.guild.get_member(self.owner_id),
            view_channel=True
        )

        await interaction.response.send_message("🔓 Ticket reabierto")


async def setup(bot):
    await bot.add_cog(Tickets(bot))
