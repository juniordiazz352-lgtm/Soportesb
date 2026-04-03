import discord
from discord.ui import View, Button
from system.ticket_system import create_ticket

class PanelView(View):
    def __init__(self, tipos):
        super().__init__(timeout=None)
        
class PanelView(View):
    @button(label="🎟️ Crear Ticket", style=discord.ButtonStyle.primary)
    async def create(self, interaction, button):
        await create_ticket(interaction.guild, interaction.user, "ticket")
        await interaction.response.send_message("Creado", ephemeral=True)
