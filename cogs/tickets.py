import discord
from discord.ext import commands
from utils.embeds import panel_embed, ticket_embed
import config

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Crear Ticket", emoji="📩", style=discord.ButtonStyle.primary, custom_id="ticket_create")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild = interaction.guild

        # ❌ Evitar duplicados
        existing = discord.utils.get(guild.text_channels, name=f"ticket-{interaction.user.name}")
        if existing:
            await interaction.response.send_message("❌ Ya tienes un ticket abierto", ephemeral=True)
            return

        # 📁 Crear categoría si no existe
        category = discord.utils.get(guild.categories, name=config.TICKET_CATEGORY)
        if not category:
            category = await guild.create_category(config.TICKET_CATEGORY)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }

        # 👮 Permiso para staff
        role = discord.utils.get(guild.roles, name=config.STAFF_ROLE)
        if role:
            overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        # 📂 Crear canal
        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category,
            overwrites=overwrites
        )

        # 🔒 Botón cerrar
        view = CloseView()

        await channel.send(embed=ticket_embed(interaction.user), view=view)

        await interaction.response.send_message("✅ Ticket creado", ephemeral=True)


class CloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Cerrar Ticket", emoji="🔒", style=discord.ButtonStyle.danger, custom_id="ticket_close")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message("🔒 Cerrando ticket...", ephemeral=True)

        # 📝 Log
        log_channel = discord.utils.get(interaction.guild.text_channels, name=config.LOG_CHANNEL)
        if log_channel:
            await log_channel.send(f"📁 Ticket cerrado por {interaction.user.mention}: {interaction.channel.name}")

        await interaction.channel.delete()


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def panel(self, ctx):
        await ctx.send(embed=panel_embed(), view=TicketView())


async def setup(bot):
    await bot.add_cog(Tickets(bot))
