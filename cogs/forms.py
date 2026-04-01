import discord
from discord.ext import commands
from discord import app_commands
import json
import config
import asyncio

def load(file):
    try:
        with open(file) as f:
            return json.load(f)
    except:
        return {}

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

class FormView(discord.ui.View):
    def __init__(self, respuestas, user):
        super().__init__(timeout=None)
        self.respuestas = respuestas
        self.user = user

    @discord.ui.button(label="✅ Aprobar", style=discord.ButtonStyle.green)
    async def aprobar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.user.send("✅ Tu formulario fue aprobado")
        await interaction.response.send_message("Aprobado", ephemeral=True)

    @discord.ui.button(label="❌ Rechazar", style=discord.ButtonStyle.red)
    async def rechazar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.user.send("❌ Tu formulario fue rechazado")
        await interaction.response.send_message("Rechazado", ephemeral=True)

class Forms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_owner(self, i):
        return i.user.id == config.OWNER_ID

    # 📋 CREAR
    @app_commands.command(name="form_crear")
    async def crear(self, i: discord.Interaction):
        if not self.is_owner(i):
            return await i.response.send_message("❌ Solo owner", ephemeral=True)

        await i.response.send_message("Título:")

        def check(m): return m.author == i.user

        titulo = (await self.bot.wait_for("message", check=check)).content

        await i.followup.send("Cantidad preguntas:")
        n = int((await self.bot.wait_for("message", check=check)).content)

        preguntas = []
        for x in range(n):
            await i.followup.send(f"Pregunta {x+1}")
            preguntas.append((await self.bot.wait_for("message", check=check)).content)

        data = load("data/forms.json")
        data[titulo] = preguntas
        save("data/forms.json", data)

        await i.followup.send("✅ Form creado")

    # 🎛️ PANEL
    @app_commands.command(name="panel_form")
    async def panel(self, i: discord.Interaction):

        data = load("data/forms.json")

        options = [discord.SelectOption(label=k) for k in data.keys()]

        class Menu(discord.ui.Select):
            def __init__(self):
                super().__init__(placeholder="Selecciona", options=options)

            async def callback(self, interaction: discord.Interaction):
                preguntas = data[self.values[0]]

                try:
                    await interaction.user.send("📋 Inicio")
                except:
                    return await interaction.response.send_message("Activa DM", ephemeral=True)

                respuestas = []

                for p in preguntas:
                    await interaction.user.send(p)
                    try:
                        msg = await interaction.client.wait_for(
                            "message",
                            timeout=180,
                            check=lambda m: m.author == interaction.user
                        )
                        respuestas.append(msg.content)
                    except:
                        respuestas.append("No respondió")

                embed = discord.Embed(title="Formulario")
                for p, r in zip(preguntas, respuestas):
                    embed.add_field(name=p, value=r, inline=False)

                await interaction.channel.send(
                    embed=embed,
                    view=FormView(respuestas, interaction.user)
                )

                await interaction.response.send_message("Enviado", ephemeral=True)

        view = discord.ui.View()
        view.add_item(Menu())

        await i.channel.send("📋 Panel formularios", view=view)
        await i.response.send_message("Panel creado", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Forms(bot))
