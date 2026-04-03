import discord
from discord.ui import Modal, TextInput
from system.form_system import get_form
from view.form_review_view import FormReviewView
from system.history_system import add_history


class DynamicForm(Modal):
    def __init__(self, guild_id, form_name):
        self.form = get_form(guild_id, form_name)
        self.form_name = form_name

        super().__init__(title=f"📋 {form_name}")

        self.inputs = []

        for q in self.form["questions"]:
            inp = TextInput(label=q, required=True, max_length=200)
            self.inputs.append(inp)
            self.add_item(inp)

    async def on_submit(self, interaction: discord.Interaction):
        channel = interaction.guild.get_channel(self.form["channel"])

        embed = discord.Embed(
            title=f"📋 Nuevo Formulario • {self.form_name}",
            description=f"👤 {interaction.user.mention}",
            color=discord.Color.orange()
        )

        respuestas_texto = ""

        for i, inp in enumerate(self.inputs, start=1):
            embed.add_field(
                name=f"📝 {i}. {inp.label}",
                value=f"```{inp.value}```",
                inline=False
            )
            respuestas_texto += f"{inp.label}: {inp.value}\n"

        embed.add_field(
            name="📊 Información",
            value=(
                f"🆔 ID: `{interaction.user.id}`\n"
                f"📅 <t:{int(discord.utils.utcnow().timestamp())}:F>"
            ),
            inline=False
        )

        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_footer(text="Sistema de Formularios • Nivel Empresa")

        # 📊 HISTORIAL
        add_history(interaction.user.id, "formulario", respuestas_texto)

        # 📤 ENVIAR A CANAL
        await channel.send(
            embed=embed,
            view=FormReviewView(interaction.user.id)
        )

        # 📩 DM
        try:
            dm_embed = discord.Embed(
                title="📨 Formulario enviado",
                description="Tu formulario fue enviado correctamente",
                color=discord.Color.green()
            )

            for inp in self.inputs:
                dm_embed.add_field(
                    name=f"📝 {inp.label}",
                    value=f"```{inp.value}```",
                    inline=False
                )

            await interaction.user.send(embed=dm_embed)

        except:
            pass

        await interaction.response.send_message(
            "✅ Formulario enviado correctamente",
            ephemeral=True
        )
