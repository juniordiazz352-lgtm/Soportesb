from discord.ext import commands
from discord import app_commands
import discord
from systems.form_system import save_form, delete_form
from views.form_views import FormPanel

class Forms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="crear_formulario")
    async def crear_formulario(self, interaction, nombre: str, preguntas: str, canal: discord.TextChannel):
        lista = [p.strip() for p in preguntas.split(",")]
        save_form(interaction.guild.id, nombre, lista, canal.id)

        await interaction.response.send_message(f"✅ Formulario {nombre} creado", ephemeral=True)

    @app_commands.command(name="eliminar_formulario")
    async def eliminar_formulario(self, interaction, nombre: str):
        delete_form(interaction.guild.id, nombre)
        await interaction.response.send_message("🗑 Formulario eliminado", ephemeral=True)

    @app_commands.command(name="panel_forms")
    async def panel_forms(self, interaction):
        view = FormPanel(interaction.guild.id)

        embed = discord.Embed(
            title="📋 Formularios",
            description="Selecciona uno:",
            color=discord.Color.blurple()
        )

        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message("✅ Panel creado", ephemeral=True)

@app_commands.command(name="historial")
async def historial(self, interaction, usuario: discord.User):
    from database.db import load

    data = load("database/responses.json")

    user_data = data.get(str(usuario.id))

    if not user_data:
        return await interaction.response.send_message("❌ Sin historial", ephemeral=True)

    embed = discord.Embed(
        title=f"📜 Historial de {usuario}",
        color=discord.Color.blurple()
    )

    for i, app in enumerate(user_data[-5:], 1):
        estado = app.get("estado", "pendiente")

        respuestas = "\n".join(
            [f"**{k}:** {v}" for k, v in app["respuestas"].items()]
        )

        embed.add_field(
            name=f"{i}. {app['form']} ({estado})",
            value=respuestas,
            inline=False
        )

    await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Forms(bot))
