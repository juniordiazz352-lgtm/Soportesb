import discord
from discord.ext import commands
from discord import app_commands
import json
import config

def load(file):
    try:
        with open(file) as f:
            return json.load(f)
    except:
        return {}

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Cerrar", style=discord.ButtonStyle.red)
    async def cerrar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.delete()

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_owner(self, i):
        return i.user.id == config.OWNER_ID

    @app_commands.command(name="agregar_rol_staff")
    async def staff(self, i: discord.Interaction, rol: discord.Role):
        if not self.is_owner(i):
            return await i.response.send_message("❌ Solo owner", ephemeral=True)

        data = load("data/staff.json")
        data[str(i.guild.id)] = rol.id
        save("data/staff.json", data)

        await i.response.send_message("✅ Staff agregado")

    @app_commands.command(name="crear_ticket")
    async def crear(self, i: discord.Interaction, nombre: str, titulo: str, descripcion: str):
        if not self.is_owner(i):
            return await i.response.send_message("❌ Solo owner", ephemeral=True)

        data = load("data/tickets.json")
        if str(i.guild.id) not in data:
            data[str(i.guild.id)] = {}

        data[str(i.guild.id)][nombre] = {
            "titulo": titulo,
            "descripcion": descripcion
        }

        save("data/tickets.json", data)
        await i.response.send_message("✅ Ticket creado")

    @app_commands.command(name="panel_ticket")
    async def panel(self, i: discord.Interaction):
        data = load("data/tickets.json").get(str(i.guild.id), {})

        options = [
            discord.SelectOption(label=k, description=v["descripcion"])
            for k, v in data.items()
        ]

        class Menu(discord.ui.Select):
            def __init__(self):
                super().__init__(placeholder="Selecciona ticket", options=options)

            async def callback(self, interaction: discord.Interaction):
                guild = interaction.guild
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    interaction.user: discord.PermissionOverwrite(read_messages=True)
                }

                channel = await guild.create_text_channel(
                    name=f"ticket-{interaction.user.name}",
                    overwrites=overwrites
                )

                await channel.send(
                    f"{interaction.user.mention}",
                    view=TicketView()
                )

                await interaction.response.send_message(f"🎫 Ticket creado: {channel.mention}", ephemeral=True)

        view = discord.ui.View()
        view.add_item(Menu())

        await i.channel.send("🎫 Panel de tickets", view=view)
        await i.response.send_message("✅ Panel creado", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Tickets(bot))
