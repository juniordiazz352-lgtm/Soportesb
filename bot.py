import discord
from discord.ext import commands
import asyncio
from config import TOKEN
from views.panel_view import PanelView
from views.ticket_controls import TicketControls
from views.form_dynamic_panel import FormPanel
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
bot.add_view(FormPanel(guild_id=0))
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🔥 Startup Bot listo: {bot.user}")

    bot.add_view(PanelView())
    bot.add_view(TicketControls(user_id=0))
    
    await bot.tree.sync()

async def main():
    async with bot:
        await bot.load_extension("commands.forms")
        await bot.load_extension("commands.setup")
        await bot.start(TOKEN)

asyncio.run(main())
