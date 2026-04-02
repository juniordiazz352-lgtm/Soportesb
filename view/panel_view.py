import discord
from discord.ui import View, Button
from system.ticket_system import create_ticket

class PanelView(View):
    def __init__(self, tipos):
        super().__init__(timeout=None)

        for tipo in tipos:
            button = Button(label=tipo, style=discord.ButtonStyle.primary)

            async def callback(interaction: discord.Interaction, t=tipo):
                await create_ticket(interaction.guild, interaction.user, t)

            button.callback = callback
            self.add_item(button)
