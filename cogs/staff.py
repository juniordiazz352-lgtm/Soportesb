import discord
from discord.ext import commands
from discord import app_commands
from database.db import add_staff_role, get_staff_roles
import config

class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_owner(self, i):
        return i.user.id == config.OWNER_ID

    @app_commands.command(name="agregar_staff")
    async def agregar_staff(self, i: discord.Interaction, rol: discord.Role):
        if not self.is_owner(i):
            return await i.response.send_message("❌ Solo owner", ephemeral=True)

        add_staff_role(str(i.guild.id), str(rol.id))
        await i.response.send_message("✅ Rol staff agregado")

async def setup(bot):
    await bot.add_cog(Staff(bot))
