import discord
from discord.ext import commands
import asyncio
from config import TOKEN, GUILD_ID
from views.panel_view import PanelView
from views.ticket_controls import TicketControls

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Conectado como {bot.user}")

    # Persistencia de botones
    bot.add_view(PanelView())
    bot.add_view(TicketControls(user_id=0))

    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))

async def main():
    async with bot:
        await bot.load_extension("commands.setup")
        await bot.start(TOKEN)

asyncio.run(main())
