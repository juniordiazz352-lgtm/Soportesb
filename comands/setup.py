from discord.ext import commands
from discord import app_commands
import discord
from view.panel_view import PanelView
from utils.embeds import panel_embed

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="panel", description="Crear panel de tickets")
    async def panel(self, interaction: discord.Interaction):
        await interaction.channel.send(embed=panel_embed(), view=PanelView())
        await interaction.response.send_message("✅ Panel creado", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Setup(bot))


from discord.ext import commands
from discord import app_commands
from database.db import load, save

GUILDS_FILE = "database/guilds.json"

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup")
    async def setup(self, interaction, staff_role: discord.Role, category: discord.CategoryChannel, logs: discord.TextChannel):
        data = load(GUILDS_FILE)

        data[str(interaction.guild.id)] = {
            "staff_role": staff_role.id,
            "category": category.id,
            "logs": logs.id
        }

        save(GUILDS_FILE, data)

        await interaction.response.send_message("✅ Configurado", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Setup(bot))
