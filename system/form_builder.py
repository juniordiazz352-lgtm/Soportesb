import discord
from database.db import load, save

FORMS_FILE = "database/forms.json"

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


# 📋 MODAL DINÁMICO
class DynamicForm(discord.ui.Modal):
    def __init__(self, form_name, preguntas, canal_id):
        super().__init__(title=f"Formulario: {form_name}")
        self.form_name = form_name
        self.canal_id = canal_id

        self.inputs = []

        for pregunta in preguntas[:5]:  # limite discord
            input_field = discord.ui.TextInput(label=pregunta)
            self.inputs.append(input_field)
            self.add_item(input_field)

    async def on_submit(self, interaction: discord.Interaction):
        canal = interaction.guild.get_channel(self.canal_id)

        embed = discord.Embed(
            title=f"📋 Formulario: {self.form_name}",
            color=discord.Color.orange()
        )

        for input_field in self.inputs:
            embed.add_field(name=input_field.label, value=input_field.value, inline=False)

        embed.add_field(name="Usuario", value=interaction.user.mention)

        await canal.send(embed=embed)

        await interaction.response.send_message("✅ Formulario enviado", ephemeral=True)
