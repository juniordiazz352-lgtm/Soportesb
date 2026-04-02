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
        await interaction.response.send_message("🗑 Eliminado", ephemeral=True)

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

async def setup(bot):
    await bot.add_cog(Forms(bot))
