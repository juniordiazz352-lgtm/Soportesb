import discord
from discord.ui import View, Select
from systems.ticket_system import create_ticket

class PanelView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

class TicketSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Soporte", emoji="🛠", description="Ayuda general"),
            discord.SelectOption(label="Ayuda general", emoji="🛡️", description="Pagos y compras"),
            discord.SelectOption(label="Reportes", emoji="⚠", description="Reportar usuarios"),
        ]
        super().__init__(placeholder="Selecciona una categoría...", options=options)

    async def callback(self, interaction: discord.Interaction):
        await create_ticket(interaction, self.values[0])
