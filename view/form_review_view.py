import discord
from discord.ui import View, button
from system.form_system import update_response_status


class FormReviewView(View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    @button(label="✅ Aprobar", style=discord.ButtonStyle.success)
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):

        update_response_status(self.user_id, "aprobado")

        user = await interaction.client.fetch_user(self.user_id)

        try:
            await user.send("✅ Tu formulario fue aprobado")
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

        await interaction.response.send_message(
            "Aprobado",
            ephemeral=True
        )

    @button(label="❌ Rechazar", style=discord.ButtonStyle.danger)
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_modal(
            RejectModal(self.user_id, interaction.message)
        )


class RejectModal(discord.ui.Modal, title="Motivo del rechazo"):
    motivo = discord.ui.TextInput(
        label="Motivo",
        style=discord.TextStyle.paragraph
    )

    def __init__(self, user_id, message):
        super().__init__()
        self.user_id = user_id
        self.message = message

    async def on_submit(self, interaction: discord.Interaction):

        update_response_status(self.user_id, "rechazado", self.motivo.value)

        user = await interaction.client.fetch_user(self.user_id)

        try:
            await user.send(
                f"❌ Rechazado\nMotivo: {self.motivo.value}"
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

        await interaction.response.send_message(
            "Rechazado",
            ephemeral=True
        )
