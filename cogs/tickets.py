import discord
from discord.ext import commands
from discord import app_commands

from utils.storage import load_data, save_data
from utils.checks import is_owner

FILE = "data/tickets.json"

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="crear_ticket")
    async def crear_ticket(self, interaction: discord.Interaction, nombre: str, titulo: str, descripcion: str):
        if not is_owner(interaction.user):
            return await interaction.response.send_message("❌ Solo dueño", ephemeral=True)

        data = load_data(FILE)
        data[nombre] = {"titulo": titulo, "descripcion": descripcion}
        save_data(FILE, data)

        await interaction.response.send_message("✅ Ticket creado", ephemeral=True)

    @app_commands.command(name="panel_ticket")
    async def panel_ticket(self, interaction: discord.Interaction):
        if not is_owner(interaction.user):
            return await interaction.response.send_message("❌ Solo dueño", ephemeral=True)

        data = load_data(FILE)

        options = [discord.SelectOption(label=k, value=k) for k in data]

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

                channel = await guild.create_text_channel(
                    name=f"ticket-{user.name}",
                    overwrites=overwrites
                )

                await inter.response.send_message("Ticket creado", ephemeral=True)
                await channel.send("Soporte", view=Buttons())

        class View(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)
                self.add_item(Select())

        await interaction.response.send_message("Panel tickets", view=View())


class Buttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Reclamar", style=discord.ButtonStyle.primary)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"Ticket reclamado por {interaction.user}")

    @discord.ui.button(label="Cerrar", style=discord.ButtonStyle.danger)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.delete()

    @discord.ui.button(label="Reabrir", style=discord.ButtonStyle.success)
    async def reopen(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Reabierto")


async def setup(bot):
    await bot.add_cog(Tickets(bot))
async def setup(bot):
    await bot.add_cog(Tickets(bot))
