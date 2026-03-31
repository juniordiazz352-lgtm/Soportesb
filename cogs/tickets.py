import discord
from discord.ext import commands
from discord import app_commands

from utils.storage import load_data, save_data
from utils.checks import is_owner
from utils.transcript import create_transcript

FILE = "data/tickets.json"
STATS = "data/stats.json"

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="agregar_rol_staff")
    async def staff(self, interaction: discord.Interaction, rol: discord.Role):
        if not is_owner(interaction.user):
            return await interaction.response.send_message("❌ Solo dueño", ephemeral=True)

        data = load_data(FILE)
        data["staff_roles"].append(rol.id)
        save_data(FILE, data)

        await interaction.response.send_message("✅ Staff agregado")

    @app_commands.command(name="crear_ticket")
    async def crear_ticket(self, interaction: discord.Interaction, nombre: str, titulo: str, descripcion: str, emoji: str):
        if not is_owner(interaction.user):
            return await interaction.response.send_message("❌ Solo dueño", ephemeral=True)

        data = load_data(FILE)
        data["tickets"][nombre] = {
            "titulo": titulo,
            "descripcion": descripcion,
            "emoji": emoji
        }
        save_data(FILE, data)

        await interaction.response.send_message("✅ Ticket creado")

    @app_commands.command(name="panel_ticket")
    async def panel(self, interaction: discord.Interaction, canal: discord.TextChannel, categoria: discord.CategoryChannel, titulo: str, descripcion: str):

        data = load_data(FILE)

        options = [
            discord.SelectOption(
                label=t["titulo"],
                description=t["descripcion"][:100],
                emoji=t["emoji"],
                value=name
            )
            for name, t in data["tickets"].items()
        ]

        class Select(discord.ui.Select):
            def __init__(self):
                super().__init__(placeholder="Selecciona ticket", options=options)

            async def callback(self, inter: discord.Interaction):
                guild = inter.guild
                user = inter.user

                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    user: discord.PermissionOverwrite(view_channel=True)
                }

                for role_id in data["staff_roles"]:
                    role = guild.get_role(role_id)
                    if role:
                        overwrites[role] = discord.PermissionOverwrite(view_channel=True)

                channel = await guild.create_text_channel(
                    name=f"ticket-{user.id}",
                    category=categoria,
                    overwrites=overwrites
                )

                await channel.send(f"🎫 Ticket de {user.mention}", view=Buttons(user.id))
                await inter.response.send_message("✅ Ticket creado", ephemeral=True)

        class View(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)
                self.add_item(Select())

        embed = discord.Embed(title=titulo, description=descripcion)
        await canal.send(embed=embed, view=View())

        await interaction.response.send_message("✅ Panel creado", ephemeral=True)


class Buttons(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    @discord.ui.button(label="Cerrar", style=discord.ButtonStyle.danger)
    async def close(self, interaction: discord.Interaction, button):
        file = await create_transcript(interaction.channel)
        await interaction.channel.send(file=discord.File(file))
        await interaction.channel.delete()


async def setup(bot):
    await bot.add_cog(Tickets(bot))
