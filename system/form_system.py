import discord
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

   data[str(user_id)].append({
    "form": form_name,
    "respuestas": respuestas,
    "estado": "pendiente"
})

    save(FORMS_FILE, data)

def delete_form(guild_id, name):
    data = load(FORMS_FILE)

    if str(guild_id) in data and name in data[str(guild_id)]:
        del data[str(guild_id)][name]

    save(FORMS_FILE, data)


# ========================
# 📨 RESPUESTAS
# ========================

def save_response(user_id, form_name, respuestas):
    data = load(RESPONSES_FILE)

    if str(user_id) not in data:
        data[str(user_id)] = []

    data[str(user_id)].append({
        "form": form_name,
        "respuestas": respuestas
    })

    save(RESPONSES_FILE, data)


# ========================
# 📋 MODAL DINÁMICO
# ========================

class DynamicForm(discord.ui.Modal):
    def __init__(self, form_name, preguntas, canal_id):
        super().__init__(title=form_name)
        self.form_name = form_name
        self.canal_id = canal_id
        self.inputs = []

        for pregunta in preguntas[:5]:
            inp = discord.ui.TextInput(label=pregunta)
            self.inputs.append(inp)
            self.add_item(inp)

    async def on_submit(self, interaction: discord.Interaction):
        canal = interaction.guild.get_channel(self.canal_id)

        respuestas = {inp.label: inp.value for inp in self.inputs}

        save_response(interaction.user.id, self.form_name, respuestas)

       from datetime import datetime

embed = discord.Embed(
    title="📋 Nueva Aplicación",
    color=discord.Color.orange(),
    timestamp=datetime.utcnow()
)

embed.add_field(name="👤 Usuario", value=interaction.user.mention, inline=True)
embed.add_field(name="📄 Formulario", value=self.form_name, inline=True)
embed.add_field(name="📊 Estado", value="🟡 Pendiente", inline=False)

respuestas_texto = "\n".join(
    [f"**{k}:** {v}" for k, v in respuestas.items()]
)

embed.add_field(
    name="🧠 Respuestas",
    value=respuestas_texto[:1024],
    inline=False
)

embed.set_footer(text=f"ID Usuario: {interaction.user.id}")

        for k, v in respuestas.items():
            embed.add_field(name=k, value=v, inline=False)

        embed.add_field(name="Usuario", value=interaction.user.mention)

        await canal.send(embed=embed, view=ReviewView(interaction.user))

        await interaction.response.send_message("✅ Formulario enviado", ephemeral=True)


# ========================
# 👮 REVIEW STAFF
# ========================

class ReviewView(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=None)
        self.user = user

    @discord.ui.button(label="Aprobar", style=discord.ButtonStyle.success)
    async def approve(self, interaction, button):
        from database.db import load, save
RESPONSES_FILE = "database/responses.json"

data = load(RESPONSES_FILE)

user_data = data.get(str(self.user.id), [])
if user_data:
    user_data[-1]["estado"] = "aprobado"

save(RESPONSES_FILE, data)
        await self.user.send("✅ Tu formulario fue aprobado")
embed = interaction.message.embeds[0]
embed.color = discord.Color.green()

for field in embed.fields:
    if field.name == "📊 Estado":
        embed.set_field_at(
            embed.fields.index(field),
            name="📊 Estado",
            value="🟢 Aprobado",
            inline=False
        )

await interaction.message.edit(embed=embed, view=None)
        await interaction.response.send_message("Aprobado", ephemeral=True)

    @discord.ui.button(label="Rechazar", style=discord.ButtonStyle.danger)
    async def reject(self, interaction, button):
        await interaction.response.send_modal(RejectModal(self.user, interaction.message))


class RejectModal(discord.ui.Modal, title="Motivo del rechazo"):
    motivo = discord.ui.TextInput(label="Motivo", style=discord.TextStyle.paragraph)

    def __init__(self, user, message):
        super().__init__()
        self.user = user
        self.message = message
        
from database.db import load, save
RESPONSES_FILE = "database/responses.json"

data = load(RESPONSES_FILE)

user_data = data.get(str(self.user.id), [])
if user_data:
    user_data[-1]["estado"] = "rechazado"

save(RESPONSES_FILE, data)

    embed = self.message.embeds[0]
embed.color = discord.Color.red()

for field in embed.fields:
    if field.name == "📊 Estado":
        embed.set_field_at(
            embed.fields.index(field),
            name="📊 Estado",
            value=f"🔴 Rechazado\nMotivo: {self.motivo.value}",
            inline=False
        )

await self.message.edit(embed=embed, view=None)

await self.user.send(f"❌ Tu formulario fue rechazado\n📌 Motivo: {self.motivo.value}")

await interaction.response.send_message("Rechazado", ephemeral=True)
