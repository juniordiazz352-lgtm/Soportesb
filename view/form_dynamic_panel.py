import discord
from discord.ui import View, Select
from systems.form_builder import get_forms, DynamicForm

class FormPanel(View):
    def __init__(self, guild_id):
        super().__init__(timeout=None)

        forms = get_forms(guild_id)

        options = [
            discord.SelectOption(label=name)
            for name in forms.keys()
        ]

        if options:
            self.add_item(FormSelect(options, forms))


class FormSelect(discord.ui.Select):
    def __init__(self, options, forms):
        super().__init__(placeholder="Selecciona formulario...", options=options)
        self.forms = forms

    async def callback(self, interaction: discord.Interaction):
        form = self.forms[self.values[0]]

        await interaction.response.send_modal(
            DynamicForm(
                self.values[0],
                form["preguntas"],
                form["canal"]
            )
        )
