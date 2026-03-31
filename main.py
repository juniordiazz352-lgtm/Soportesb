import discord
from discord.ext import commands
import asyncio
import config
import threading
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot activo"

def run_web():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web).start()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🔥 {bot.user} listo")

    try:
        synced = await bot.tree.sync()
        print(f"Comandos: {len(synced)}")
    except Exception as e:
        print(e)

async def main():
    async with bot:
        await bot.load_extension("cogs.forms")
        await bot.load_extension("cogs.tickets")
        await bot.start(config.TOKEN)

asyncio.run(main())
