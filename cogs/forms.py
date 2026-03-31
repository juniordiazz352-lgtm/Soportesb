import discord
from discord.ext import commands
from discord import app_commands
import asyncio

from utils.storage import load_data, save_data
from utils.checks import is_owner

FILE = "data/forms.json"

class Forms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🔧 CREAR FORMULARIO PRO
    @app_commands.command(name="crear_formulario")
    async def crear_formulario(self, interaction: discord.Interaction):

        if not is_owner(interaction.user):
            return await interaction.response.send_message("❌ Solo dueño", ephemeral=True)

        await interaction.response.send_message("📝 Título del formulario:", ephemeral=True)

        def check(m): return m.author == interaction.user

        msg = await self.bot.wait_for("message", check=check)
        titulo = msg.content

        await interaction.followup.send("❓ Número de preguntas:", ephemeral=True)
        msg = await self.bot.wait_for("message", check=check)
        cantidad = int(msg.content)

        preguntas = []

        for i in range(cantidad):
            await interaction.followup.send(f"✏️ Pregunta {i+1}:", ephemeral=True)
            msg = await self.bot.wait_for("message", check=check)
            preguntas.append(msg.content)

        # CONFIRMAR
        confirm_msg = await interaction.followup.send(
            "✅ ¿Terminar formulario?\n👍 = sí | ❌ = cancelar",
            ephemeral=True
        )

        await confirm_msg.add_reaction("👍")
        await confirm_msg.add_reaction("❌")

        def reaction_check(reaction, user):
            return user == interaction.user and str(reaction.emoji) in ["👍", "❌"]

        reaction, _ = await self.bot.wait_for("reaction_add", check=reaction_check)

        if str(reaction.emoji) == "❌":
            return await interaction.followup.send("❌ Cancelado", ephemeral=True)

        data = load_data(FILE)
        form_id = str(len(data) + 1)

        data[form_id] = {
            "titulo": titulo,
            "preguntas": preguntas
        }

        save_data(FILE, data)

        await interaction.followup.send(f"✅ Formulario creado ID: {form_id}", ephemeral=True)

    # 📊 PANEL PRO
    @app_commands.command(name="panel_formularios")
    async def panel_formularios(self, interaction: discord.Interaction, canal: discord.TextChannel, descripcion: str):

        if not is_owner(interaction.user):
            return await interaction.response.send_message("❌ Solo dueño", ephemeral=True)

        data = load_data(FILE)

        options = [
            discord.SelectOption(label=f["titulo"], value=form_id)
            for form_id, f in data.items()
        ]

        class Select(discord.ui.Select):
            def __init__(self, bot):
                super().__init__(placeholder="Selecciona formulario", options=options)
                self.bot = bot

            async def callback(self, inter: discord.Interaction):

                user = inter.user
                form = data[self.values[0]]

                await inter.response.send_message("📩 Revisa tu DM", ephemeral=True)

                respuestas = []

                for pregunta in form["preguntas"]:
                    try:
                        await user.send(f"❓ {pregunta}")

                        def check(m):
                            return m.author == user and isinstance(m.channel, discord.DMChannel)

                        msg = await self.bot.wait_for("message", timeout=180, check=check)
                        respuestas.append(msg.content)

                    except asyncio.TimeoutError:
                        respuestas.append("⏱️ Sin respuesta")

                embed = discord.Embed(
                    title=f"📨 {form['titulo']}",
                    description="\n".join(respuestas),
                    color=discord.Color.blurple()
                )

                view = ReviewView(user, form, respuestas)

                await canal.send(embed=embed, view=view)

        class View(discord.ui.View):
            def __init__(self, bot):
                super().__init__(timeout=None)
                self.add_item(Select(bot))

        embed = discord.Embed(title="📋 Formularios", description=descripcion)

        await interaction.response.send_message("✅ Panel creado", ephemeral=True)
        await canal.send(embed=embed, view=View(self.bot))
