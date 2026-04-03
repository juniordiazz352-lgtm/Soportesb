import discord
from discord.ui import View, button
import asyncio

from system.transcript_system import generate_transcript


class TicketControls(View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    @button(label="🔒 Cerrar", style=discord.ButtonStyle.danger)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):

        # 🔒 SOLO STAFF
        if not interaction.user.guild_permissions.manage_channels:
            return await interaction.response.send_message(
                "❌ No tienes permisos",
                ephemeral=True
            )

        await interaction.response.send_message(
            "⏳ Generando transcript...",
            ephemeral=True
        )

        try:
            # 📄 GENERAR TRANSCRIPT
            transcript = await generate_transcript(interaction.channel)

            # 📂 CANAL LOGS
            log_channel = discord.utils.get(
                interaction.guild.text_channels,
                name="ticket-logs"
            )

            if not log_channel:
                log_channel = await interaction.guild.create_text_channel("ticket-logs")

            await log_channel.send(
                content=f"📁 Transcript de {interaction.channel.name}",
                file=transcript
            )

        except Exception as e:
            print("❌ ERROR TRANSCRIPT:", e)

        await asyncio.sleep(1)
        await interaction.channel.delete()
        text = "\n".join(reversed(messages))[:1900]

        await interaction.user.send(f"```{text}```")
        await interaction.response.send_message("📄 Enviado por DM", ephemeral=True)
