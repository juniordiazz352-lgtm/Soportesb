import discord
from discord.ui import View, Button
from view.dynamic_form_modal import DynamicForm

class FormPanel(View):
    def __init__(self, guild_id, form_name):
        super().__init__(timeout=None)

        button = Button(label=form_name, style=discord.ButtonStyle.success)

        async def callback(interaction: discord.Interaction):
            await interaction.response.send_modal(
                DynamicForm(guild_id, form_name)
            )

        button.callback = callback
        self.add_item(button)
