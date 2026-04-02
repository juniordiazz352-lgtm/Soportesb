from discord.ext import commands
from discord import app_commands
import discord
from views.panel_view import PanelView
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
