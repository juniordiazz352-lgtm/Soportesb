import discord
from discord.ext import commands
from discord import app_commands

from utils.storage import load_data, save_data
from utils.checks import is_owner

FILE = "data/tickets.json"

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🧱 CREAR TIPO DE TICKET
    @app_commands.command(name="crear_ticket")
    async def crear_ticket(
        self,
        interaction: discord.Interaction,
        nombre: str,
        titulo: str,
        descripcion: str
    ):
        if not is_owner(interaction.user):
            return await interaction.response.send_message("❌ Solo dueño", ephemeral=True)

        data = load_data(FILE)

        data[nombre] = {
            "titulo": titulo,
            "descripcion": descripcion
        }

        save_data(FILE, data)

        await interaction.response.send_message("✅ Tipo de ticket creado", ephemeral=True)

    # 📊 PANEL DE TICKETS
    @app_commands.command(name="panel_ticket")
    async def panel_ticket(
        self,
        interaction: discord.Interaction,
        canal: discord.TextChannel,
        categoria: discord.CategoryChannel,
        descripcion: str
    ):
        if not is_owner(interaction.user):
            return await interaction.response.send_message("❌ Solo dueño", ephemeral=True)

        data = load_data(FILE)

        options = [
            discord.SelectOption(label=k, value=k)
            for k in data
        ]

        class TicketSelect(discord.ui.Select):
            def __init__(self, bot):
                super().__init__(placeholder="Selecciona ticket", options=options)
                self.bot = bot

            async def callback(self, inter: discord.Interaction):
                guild = inter.guild
                user = inter.user

                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    user: discord.PermissionOverwrite(view_channel=True, send_messages=True)
                }

                # 👮 añadir staff automáticamente
                for role in guild.roles:
                    if "staff" in role.name.lower():
                        overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

                channel = await guild.create_text_channel(
                    name=f"ticket-{user.name}",
                    category=categoria,
                    overwrites=overwrites
                )

                await inter.response.send_message("✅ Ticket creado", ephemeral=True)

                embed = discord.Embed(
                    title=data[self.values[0]]["titulo"],
                    description=data[self.values[0]]["descripcion"],
                    color=discord.Color.blurple()
                )

                await channel.send(
                    content=f"🎫 Ticket de {user.mention}",
                    embed=embed,
                    view=TicketButtons()
                )

        class Panel(discord.ui.View):
            def __init__(self, bot):
                super().__init__(timeout=None)
                self.add_item(TicketSelect(bot))

        embed = discord.Embed(title="🎫 Tickets", description=descripcion)

        await interaction.response.send_message("✅ Panel creado", ephemeral=True)
        await canal.send(embed=embed, view=Panel(self.bot))


# 🔘 BOTONES
class TicketButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.claimed_by = None

    @discord.ui.button(label="Reclamar", emoji="👤", style=discord.ButtonStyle.primary)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):

        self.claimed_by = interaction.user
        await interaction.response.send_message(f"👤 Ticket reclamado por {interaction.user.mention}")

    @discord.ui.button(label="Cerrar", emoji="🔒", style=discord.ButtonStyle.danger)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message("🔒 Ticket cerrado")

        # quitar acceso al usuario
        await interaction.channel.set_permissions(interaction.user, view_channel=False)

        await interaction.channel.send("🔒 Ticket cerrado", view=ReopenButton())

    @discord.ui.button(label="Reabrir", emoji="🔓", style=discord.ButtonStyle.success)
    async def reopen(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.channel.set_permissions(interaction.user, view_channel=True)
        await interaction.response.send_message("🔓 Ticket reabierto")


# 🔓 BOTÓN REABRIR
class ReopenButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Reabrir", style=discord.ButtonStyle.success)
    async def reopen(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.set_permissions(interaction.user, view_channel=True)
        await interaction.response.send_message("🔓 Ticket reabierto")


# ➕ COMANDO AÑADIR USUARIO/ROL
class AddUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="añadir")
    async def añadir(
        self,
        interaction: discord.Interaction,
        usuario: discord.Member = None,
        rol: discord.Role = None
    ):
        if not is_owner(interaction.user):
            return await interaction.response.send_message("❌ Solo dueño", ephemeral=True)

        if usuario:
            await interaction.channel.set_permissions(
                usuario,
                view_channel=True,
                send_messages=True
            )
            await interaction.response.send_message(f"✅ {usuario.mention} añadido")

        elif rol:
            await interaction.channel.set_permissions(
                rol,
                view_channel=True,
                send_messages=True
            )
            await interaction.response.send_message(f"✅ Rol {rol.name} añadido")

        else:
            await interaction.response.send_message("❌ Debes poner usuario o rol", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Tickets(bot))
    await bot.add_cog(AddUser(bot))
