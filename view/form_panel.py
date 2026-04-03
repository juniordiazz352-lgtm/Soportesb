import discord
from discord.ui import View, Button
from view.dynamic_form_modal import DynamicForm

class FormPanel(View):
    def __init__(self, guild_id, name):
        super().__init__(timeout=None)

        btn = Button(label=name)

        async def callback(interaction):
            await interaction.response.send_modal(
                DynamicForm(guild_id, name)
            )

        btn.callback = callback
        self.add_item(btn)
