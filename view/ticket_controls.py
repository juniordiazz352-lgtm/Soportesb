import discord
import asyncio
from discord.ui import View, button

class TicketControls(View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id
        self.claimed_by = None

    # 🔒 CERRAR TICKET
    @button(label="Cerrar", style=discord.ButtonStyle.danger, emoji="🔒")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "🔒 Cerrando ticket...",
            ephemeral=True
        )

        await interaction.channel.send("🔒 El ticket será cerrado en 5 segundos...")
        await asyncio.sleep(5)(discord.utils.utcnow() + discord.timedelta(seconds=5))

        await interaction.channel.delete()

    # 👨‍💼 RECLAMAR TICKET
    @button(label="Reclamar", style=discord.ButtonStyle.primary, emoji="👨‍💼")
    async def claim_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.claimed_by:
            return await interaction.response.send_message(
                f"⚠️ Ya fue reclamado por <@{self.claimed_by}>",
                ephemeral=True
            )

        self.claimed_by = interaction.user.id

        await interaction.response.send_message(
            f"✅ Ticket reclamado por {interaction.user.mention}",
            ephemeral=False
        )

        await interaction.channel.send(
            f"👨‍💼 {interaction.user.mention} ahora está atendiendo este ticket."
        )

    # 🗑️ ELIMINAR TICKET
    @button(label="Eliminar", style=discord.ButtonStyle.secondary, emoji="🗑️")
    async def delete_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "🗑️ Eliminando ticket...",
            ephemeral=True
        )

        await interaction.channel.delete()

    # 📄 TRANSCRIPCIÓN SIMPLE
    @button(label="Transcripción", style=discord.ButtonStyle.success, emoji="📄")
    async def transcript(self, interaction: discord.Interaction, button: discord.ui.Button):
        messages = []
        async for msg in interaction.channel.history(limit=100):
            messages.append(f"{msg.author}: {msg.content}")

        transcript_text = "\n".join(reversed(messages))

        await interaction.user.send(
            f"📄 Transcripción del ticket:\n```{transcript_text[:1900]}```"
        )

        await interaction.response.send_message(
            "📄 Transcripción enviada por DM",
            ephemeral=True
        )
