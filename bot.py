import discord
from discord.ext import commands
import asyncio
import config

import threading
from flask import Flask
import os

# 🌐 Render fix
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot activo"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

threading.Thread(target=run).start()

# 🤖 Bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🔥 {bot.user} listo")
    await bot.tree.sync()

async def main():
    async with bot:
        await bot.load_extension("cogs.tickets")
        await bot.load_extension("cogs.forms")
        await bot.start(config.TOKEN)

asyncio.run(main())
