import discord
from discord.ui import View
from systems.transcript import generate_transcript
from systems.ticket_system import remove_ticket
from config import STAFF_ROLE_ID

class TicketControls(View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    @discord.ui.button(label="Reclamar", emoji="👤", style=discord.ButtonStyle.primary)
    async def claim(self, interaction, button):
        if not any(r.id == STAFF_ROLE_ID for r in interaction.user.roles):
            return await interaction.response.send_message("❌ No eres staff.", ephemeral=True)

        await interaction.response.send_message(f"👤 Ticket reclamado por {interaction.user.mention}")

    @discord.ui.button(label="Cerrar", emoji="🔒", style=discord.ButtonStyle.danger)
    async def close(self, interaction, button):
        await interaction.response.send_message("🔒 Cerrando ticket...", ephemeral=True)

        await generate_transcript(interaction.channel)

        remove_ticket(self.user_id)

        await interaction.channel.delete()
