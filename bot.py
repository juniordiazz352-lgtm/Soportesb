import discord
from discord.ext import commands
import asyncio
from config import TOKEN
from view.panel_view import PanelView
from view.ticket_controls import TicketControls
from view.form_dynamic_panel import FormPanel
import sys
import os
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise Exception("❌ TOKEN no encontrado")

bot.run(TOKEN)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 👇 FORZAR RUTA CORRECTA
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR))

print("📂 PATH DEBUG:", sys.path)
print("📂 ARCHIVOS:", os.listdir(BASE_DIR))
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

@bot.event
async def on_command_error(ctx, error):
    print("ERROR:", error)

async def main():
    async with bot:
        await bot.load_extension("comands.forms")
        await bot.load_extension("comands.setup")
        await bot.start(TOKEN)

asyncio.run(main())
