import discord
from discord.ext import commands
import os

from view.panel_view import PanelView
from view.form_panel import FormPanel
from utils.embeds import panel_embed
from system.form_system import save_form

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.getenv("TOKEN")

@bot.event
async def on_ready():
    print("Bot listo")


@bot.command()
async def panel_multi(ctx, *, opciones):
    tipos = [t.strip() for t in opciones.split(",")]
    await ctx.send(embed=panel_embed("Tickets", "Elige"), view=PanelView(tipos))


@bot.command()
async def crear_form(ctx, nombre: str, canal: discord.TextChannel, *, preguntas):
    preguntas_lista = [p.strip() for p in preguntas.split("|")]
    create_form(ctx.guild.id, nombre, preguntas_lista, canal.id)
    await ctx.send("Formulario creado")


@bot.command()
async def panel_form(ctx, nombre: str):
    await ctx.send("Formulario", view=FormPanel(ctx.guild.id, nombre))


bot.run(TOKEN)
