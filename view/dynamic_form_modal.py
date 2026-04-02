import discord
from discord.ui import Modal, TextInput
from system.form_system import get_form

class DynamicForm(Modal):
    def __init__(self, guild_id, form_name):
        self.form = get_form(guild_id, form_name)
        self.form_name = form_name

        super().__init__(title=f"Formulario: {form_name}")

        self.inputs = []

        for q in self.form["questions"]:
            inp = TextInput(label=q, required=True, max_length=200)
            self.inputs.append(inp)
            self.add_item(inp)

    async def on_submit(self, interaction: discord.Interaction):
        channel = interaction.guild.get_channel(self.form["channel"])

        embed = discord.Embed(
            title=f"📋 Formulario: {self.form_name}",
            color=discord.Color.orange()
        )

        for inp in self.inputs:
            embed.add_field(name=inp.label, value=inp.value, inline=False)

        embed.set_footer(text=f"Usuario: {interaction.user} | ID: {interaction.user.id}")

        # 📤 ENVÍA AL CANAL
        await channel.send(embed=embed)

        # 📩 ENVÍA AL DM DEL USUARIO
        try:
            await interaction.user.send(embed=embed)
        except:
            pass

        await interaction.response.send_message(
            "✅ Formulario enviado correctamente",
            ephemeral=True
        )
