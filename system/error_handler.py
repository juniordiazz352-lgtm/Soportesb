import traceback
import discord

async def handle_error(interaction=None, error=None):
    print("❌ ERROR DETECTADO:")
    traceback.print_exc()

    if interaction:
        try:
            await interaction.response.send_message(
                "❌ Ocurrió un error inesperado. El staff fue notificado.",
                ephemeral=True
            )
        except:
            pass
