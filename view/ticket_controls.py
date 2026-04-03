import discord
from discord.ui import View, button
import asyncio
from system.transcript_system import generate_transcript

class TicketControls(View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id
        self.claimed_by = None

   @button(label="🔒 Cerrar", style=discord.ButtonStyle.danger)
async def close(self, interaction: discord.Interaction, button: discord.ui.Button):

    if not interaction.user.guild_permissions.manage_channels:
        return await interaction.response.send_message("❌ Sin permisos", ephemeral=True)

    await interaction.response.send_message("⏳ Generando transcript...", ephemeral=True)

    # 📄 GENERAR HTML
    transcript = await generate_transcript(interaction.channel)

    # 📂 LOG CHANNEL
    log_channel = discord.utils.get(interaction.guild.text_channels, name="ticket-logs")

    if not log_channel:
        log_channel = await interaction.guild.create_text_channel("ticket-logs")

    await log_channel.send(
        content=f"📁 Transcript de {interaction.channel.name}",
        file=transcript
    )

    await interaction.channel.delete()

    @button(label="👨‍💼 Reclamar", style=discord.ButtonStyle.primary)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.claimed_by:
            return await interaction.response.send_message("⚠️ Ya fue reclamado", ephemeral=True)

        self.claimed_by = interaction.user.id
        await interaction.response.send_message(f"👨‍💼 {interaction.user.mention} tomó el ticket")

    @button(label="🗑️ Eliminar", style=discord.ButtonStyle.secondary)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.manage_channels:
            return await interaction.response.send_message("❌ Sin permisos", ephemeral=True)

        await interaction.channel.delete()

    @button(label="📄 Transcripción", style=discord.ButtonStyle.success)
    async def transcript(self, interaction: discord.Interaction, button: discord.ui.Button):
        messages = []
        async for msg in interaction.channel.history(limit=100):
            messages.append(f"{msg.author}: {msg.content}")

        text = "\n".join(reversed(messages))[:1900]

        await interaction.user.send(f"```{text}```")
        await interaction.response.send_message("📄 Enviado por DM", ephemeral=True)
