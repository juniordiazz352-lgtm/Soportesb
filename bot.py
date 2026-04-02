
import discord
from discord.ext import commands
from view.panel_view import PanelView
from utils.embeds import panel_embed
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.getenv("TOKEN")

@bot.event
async def on_ready():
    print(f"✅ Bot listo como {bot.user}")


# 🔥 CREAR PANEL MULTI BOTONES
@bot.command()
@commands.has_permissions(administrator=True)
async def panel_multi(ctx, *, opciones):
    tipos = [t.strip() for t in opciones.split(",")]

    embed = panel_embed(
        "🎟️ Sistema de Tickets",
        "Selecciona una opción:"
    )

    await ctx.send(
        embed=embed,
        view=PanelView(tipos)
    )


bot.run(TOKEN)
