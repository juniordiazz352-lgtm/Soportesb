import discord
from discord.ext import commands
from discord import app_commands
import asyncio

from utils.storage import load_data, save_data
from utils.checks import is_owner

FORMS_FILE = "data/forms.json"

class Forms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # CREAR FORMULARIO
    @app_commands.command(name="crear_formulario")
    async def crear_formulario(self, interaction: discord.Interaction):
        if not is_owner(interaction.user):
            return await interaction.response.send_message("❌ Solo el dueño", ephemeral=True)

        await interaction.response.send_message("📌 Escribe el título", ephemeral=True)

        def check(m): return m.author == interaction.user

        msg = await self.bot.wait_for("message", check=check)
        titulo = msg.content

        await interaction.followup.send("❓ ¿Cuántas preguntas?", ephemeral=True)
        msg = await self.bot.wait_for("message", check=check)
        cantidad = int(msg.content)

        preguntas = []
        for i in range(cantidad):
            await interaction.followup.send(f"Pregunta {i+1}", ephemeral=True)
            msg = await self.bot.wait_for("message", check=check)
            preguntas.append(msg.content)

        data = load_data(FORMS_FILE)
        form_id = str(len(data) + 1)

        data[form_id] = {"titulo": titulo, "preguntas": preguntas}
        save_data(FORMS_FILE, data)

        await interaction.followup.send(f"✅ Formulario creado ID: {form_id}", ephemeral=True)

    # PANEL FORMULARIOS
    @app_commands.command(name="panel_formularios")
    async def panel(self, interaction: discord.Interaction, descripcion: str):
        if not is_owner(interaction.user):
            return await interaction.response.send_message("❌ Solo el dueño", ephemeral=True)

        data = load_data(FORMS_FILE)

        options = [
            discord.SelectOption(label=f["titulo"], value=form_id)
            for form_id, f in data.items()
        ]

        class Select(discord.ui.Select):
            def __init__(self):
                super().__init__(placeholder="Selecciona formulario", options=options)

            async def callback(self, inter: discord.Interaction):
                user = inter.user
                form = data[self.values[0]]

                await inter.response.send_message("📩 Mira tu DM", ephemeral=True)

                respuestas = []

                for pregunta in form["preguntas"]:
                    try:
                        await user.send(pregunta)

                        def check(m):
                            return m.author == user and isinstance(m.channel, discord.DMChannel)

                        msg = await self.view.bot.wait_for("message", timeout=180, check=check)
                        respuestas.append(msg.content)

                    except asyncio.TimeoutError:
                        respuestas.append("⏱️ Sin respuesta")

                embed = discord.Embed(
                    title=form["titulo"],
                    description="\n".join(respuestas)
                )

                await inter.channel.send(embed=embed, view=ReviewView(user))

        class View(discord.ui.View):
            def __init__(self, bot):
                super().__init__(timeout=None)
                self.bot = bot
                self.add_item(Select())

        embed = discord.Embed(title="Formularios", description=descripcion)
        await interaction.response.send_message(embed=embed, view=View(self.bot))


class ReviewView(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=None)
        self.user = user

    @discord.ui.button(label="Aprobar", style=discord.ButtonStyle.success)
    async def aprobar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.user.send(f"✅ Aprobado por {interaction.user}")
        await interaction.message.delete()

    @discord.ui.button(label="Rechazar", style=discord.ButtonStyle.danger)
    async def rechazar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.user.send(f"❌ Rechazado por {interaction.user}")
        await interaction.message.delete()


async def setup(bot):
    await bot.add_cog(Forms(bot))
