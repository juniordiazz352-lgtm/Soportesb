import discord
from discord.ext import commands
import config
import asyncio
import config
from discord import app_commands

@bot.tree.interaction_check
async def global_check(interaction):
    if interaction.user.id != config.OWNER_ID:
        await interaction.response.send_message(
            "❌ Este bot es privado.",
            ephemeral=True
        )
        return False
    return True

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

    # 🔥 IMPORTANTE: mantener botones activos
    from cogs.tickets import TicketView, CloseView
    bot.add_view(TicketView())
    bot.add_view(CloseView())

@bot.event
async def on_ready():
    print(f"{bot.user} listo")

    try:
        synced = await bot.tree.sync()
        print(f"Comandos sincronizados: {len(synced)}")
    except Exception as e:
        print(e)


# ⚠️ Manejo de errores global
@bot.event
async def on_command_error(ctx, error):
    print(error)
    await ctx.send("❌ Ocurrió un error.")


async def main():
    async with bot:
        await bot.load_extension("cogs.tickets")
        await bot.start(config.TOKEN)

asyncio.run(main())
