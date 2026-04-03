import discord
from discord.ui import Modal, TextInput, View, button
from datetime import datetime
from database.db import load, save

FORMS_FILE = "database/forms.json"
RESPONSES_FILE = "database/responses.json"


# ========================
# 📋 FORMULARIOS
# ========================

def get_forms(guild_id):
    data = load(FORMS_FILE)
    return data.get(str(guild_id), {})


def save_form(guild_id, name, preguntas, canal_id):
    data = load(FORMS_FILE)

    if str(guild_id) not in data:
        data[str(guild_id)] = {}

    data[str(guild_id)][name] = {
        "preguntas": preguntas,
        "canal": canal_id
    }

    save(FORMS_FILE, data)


def get_form(guild_id, name):
    data = load(FORMS_FILE)
    return data.get(str(guild_id), {}).get(name)


# ========================
# 📨 RESPUESTAS
# ========================

def save_response(user_id, form_name, respuestas):
    data = load(RESPONSES_FILE)

    if str(user_id) not in data:
        data[str(user_id)] = []

    data[str(user_id)].append({
        "form": form_name,
        "respuestas": respuestas,
        "estado": "pendiente",
        "fecha": datetime.utcnow().isoformat()
    })

    save(RESPONSES_FILE, data)


def update_response_status(user_id, status, motivo=None):
    data = load(RESPONSES_FILE)

    user_data = data.get(str(user_id), [])
    if user_data:
        user_data[-1]["estado"] = status
        if motivo:
            user_data[-1]["motivo"] = motivo

    save(RESPONSES_FILE, data)


# ========================
# 📋 MODAL DINÁMICO
# ========================

class DynamicForm(Modal):
    def __init__(self, guild_id, form_name):
        form = get_form(guild_id, form_name)

        super().__init__(title=f"📋 {form_name}")

        self.form_name = form_name
        self.canal_id = form["canal"]
        self.inputs = []

        for pregunta in form["preguntas"][:5]:
            inp = TextInput(label=pregunta, required=True)
            self.inputs.append(inp)
            self.add_item(inp)

    async def on_submit(self, interaction: discord.Interaction):
        canal = interaction.guild.get_channel(self.canal_id)

        if not canal:
            return await interaction.response.send_message(
                "❌ Canal no encontrado",
                ephemeral=True
            )

        respuestas = {inp.label: inp.value for inp in self.inputs}

        # 💾 GUARDAR
        save_response(interaction.user.id, self.form_name, respuestas)

        # 🎨 EMBED PRO
        embed = discord.Embed(
            title="📋 Nueva Aplicación",
            color=discord.Color.orange(),
            timestamp=datetime.utcnow()
        )

        embed.set_author(
            name=f"{interaction.user}",
            icon_url=interaction.user.display_avatar.url
        )

        embed.set_thumbnail(url=interaction.user.display_avatar.url)

        embed.add_field(
            name="👤 Usuario",
            value=f"{interaction.user.mention}\n`{interaction.user.id}`",
            inline=True
        )

        embed.add_field(
            name="📄 Formulario",
            value=f"`{self.form_name}`",
            inline=True
        )

        embed.add_field(
            name="📊 Estado",
            value="🟡 Pendiente",
            inline=False
        )

        for k, v in respuestas.items():
            embed.add_field(
                name=f"📝 {k}",
                value=f"```{v[:1000]}```",
                inline=False
            )

        embed.set_footer(text="Sistema • Formularios")

        await canal.send(
            embed=embed,
            view=ReviewView(interaction.user)
        )

        # 📩 DM
        try:
            await interaction.user.send("📨 Tu formulario fue enviado")
        except:
            pass

        await interaction.response.send_message(
            "✅ Formulario enviado",
            ephemeral=True
        )


# ========================
# 👮 REVIEW STAFF
# ========================

class ReviewView(View):
    def __init__(self, user):
        super().__init__(timeout=None)
        self.user = user

    @button(label="✅ Aprobar", style=discord.ButtonStyle.success)
    async def approve(self, interaction, button):

        update_response_status(self.user.id, "aprobado")

        try:
            await self.user.send("✅ Tu formulario fue aprobado")
        except:
            pass

        embed = interaction.message.embeds[0]
        embed.color = discord.Color.green()

        for i, field in enumerate(embed.fields):
            if field.name == "📊 Estado":
                embed.set_field_at(
                    i,
                    name="📊 Estado",
                    value="🟢 Aprobado",
                    inline=False
                )

        await interaction.message.edit(embed=embed, view=None)
        await interaction.response.send_message("Aprobado", ephemeral=True)

    @button(label="❌ Rechazar", style=discord.ButtonStyle.danger)
    async def reject(self, interaction, button):
        await interaction.response.send_modal(
            RejectModal(self.user, interaction.message)
        )


class RejectModal(Modal, title="Motivo del rechazo"):
    motivo = TextInput(label="Motivo", style=discord.TextStyle.paragraph)

    def __init__(self, user, message):
        super().__init__()
        self.user = user
        self.message = message

    async def on_submit(self, interaction: discord.Interaction):

        update_response_status(self.user.id, "rechazado", self.motivo.value)

        try:
            await self.user.send(
                f"❌ Rechazado\n📌 Motivo: {self.motivo.value}"
            )
        except:
            pass

        embed = self.message.embeds[0]
        embed.color = discord.Color.red()

        for i, field in enumerate(embed.fields):
            if field.name == "📊 Estado":
                embed.set_field_at(
                    i,
                    name="📊 Estado",
                    value=f"🔴 Rechazado\n{self.motivo.value}",
                    inline=False
                )

        await self.message.edit(embed=embed, view=None)
        await interaction.response.send_message("Rechazado", ephemeral=True)
