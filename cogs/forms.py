import discord
from discord.ext import commands
from discord import app_commands
from database.db import add_form, get_forms
import config
import json
import asyncio

class Forms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_owner(self, i):
        return i.user.id == config.OWNER_ID

    # =========================
    # 📋 CREAR FORMULARIO
    # =========================
    @app_commands.command(name="crear_form")
    async def crear_form(self, i: discord.Interaction, titulo: str):
        if not self.is_owner(i):
            return await i.response.send_message("❌ Solo owner", ephemeral=True)

        await i.response.send_message("✍️ Escribe las preguntas (una por mensaje). Escribe `fin` para terminar.")

        preguntas = []

        while True:
            try:
                msg = await self.bot.wait_for(
                    "message",
                    timeout=120,
                    check=lambda m: m.author == i.user
                )
            except asyncio.TimeoutError:
                break

            if msg.content.lower() == "fin":
                break

            preguntas.append(msg.content)

        if not preguntas:
            return await i.followup.send("❌ No agregaste preguntas")

        add_form(titulo, json.dumps(preguntas))

        await i.followup.send("✅ Formulario creado")

    # =========================
    # 🗑️ BORRAR FORMULARIO
    # =========================
    @app_commands.command(name="borrar_form")
    async def borrar_form(self, i: discord.Interaction, nombre: str):
        if not self.is_owner(i):
            return await i.response.send_message("❌ Solo owner", ephemeral=True)

        from database.db import cursor, conn

        cursor.execute("DELETE FROM forms WHERE titulo=?", (nombre,))
        conn.commit()

        await i.response.send_message("🗑️ Formulario eliminado")

    # =========================
    # 📄 LISTAR FORMULARIOS
    # =========================
    @app_commands.command(name="listar_forms")
    async def listar_forms(self, i: discord.Interaction):

        data = get_forms()

        if not data:
            return await i.response.send_message("❌ No hay formularios", ephemeral=True)

        text = "\n".join([f"• {f[0]}" for f in data])

        await i.response.send_message(f"📋 Formularios:\n{text}")

    # =========================
    # 🎛️ PANEL FORMULARIOS
    # =========================
    @app_commands.command(name="panel_form")
    async def panel(self, i: discord.Interaction):

        data = get_forms()

        if not data:
            return await i.response.send_message("❌ No hay formularios", ephemeral=True)

        options = [
            discord.SelectOption(label=f[0])
            for f in data
        ]

        class Menu(discord.ui.Select):
            def __init__(self):
                super().__init__(placeholder="Selecciona formulario", options=options)

            async def callback(self, interaction: discord.Interaction):

                for f in data:
                    if f[0] == self.values[0]:
                        preguntas = json.loads(f[1])

                await interaction.user.send(f"📋 Formulario: {self.values[0]}")

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

                embed = discord.Embed(title="📋 Respuestas")

                for p, r in zip(preguntas, respuestas):
                    embed.add_field(name=p, value=r, inline=False)

                await interaction.channel.send(embed=embed)

                await interaction.response.send_message("✅ Formulario enviado", ephemeral=True)

        view = discord.ui.View()
        view.add_item(Menu())

        await i.channel.send("📋 Panel de formularios", view=view)
        await i.response.send_message("✅ Panel enviado", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Forms(bot))

class ReviewView(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=None)
        self.user = user

    @discord.ui.button(label="✅ Aprobar", style=discord.ButtonStyle.green)
    async def aprobar(self, interaction: discord.Interaction, button: discord.ui.Button):

        await self.user.send("✅ Tu formulario fue aprobado")
        await interaction.response.send_message("Aprobado")

    @discord.ui.button(label="❌ Rechazar", style=discord.ButtonStyle.red)
    async def rechazar(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message("Escribe la razón")

        msg = await interaction.client.wait_for(
            "message",
            check=lambda m: m.author == interaction.user
        )

        await self.user.send(f"❌ Rechazado\nRazón: {msg.content}")
