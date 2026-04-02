from discord.ext import commands
from discord import app_commands
import discord
from systems.form_builder import save_form
from views.form_dynamic_panel import FormPanel

class Forms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="crear_formulario", description="Crear formulario dinámico")
    async def crear_formulario(
        self,
        interaction: discord.Interaction,
        nombre: str,
        preguntas: str,
        canal: discord.TextChannel
    ):
        preguntas_lista = [p.strip() for p in preguntas.split(",")]

        save_form(interaction.guild.id, nombre, preguntas_lista, canal.id)

        await interaction.response.send_message(f"✅ Formulario '{nombre}' creado", ephemeral=True)

    @app_commands.command(name="panel_forms", description="Crear panel de formularios")
    async def panel_forms(self, interaction: discord.Interaction):
        view = FormPanel(interaction.guild.id)

        embed = discord.Embed(
            title="📋 Formularios",
            description="Selecciona un formulario del menú.",
            color=discord.Color.blurple()
        )

        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message("✅ Panel creado", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Forms(bot))
