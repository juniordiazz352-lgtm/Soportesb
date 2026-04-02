from database.db import load

GUILDS_FILE = "database/guilds.json"

async def generate_transcript(channel):
    messages = [msg async for msg in channel.history(limit=None)]

    html = "<html><body>"
    for msg in reversed(messages):
        html += f"<p><b>{msg.author}</b>: {msg.content}</p>"
    html += "</body></html>"

    file_name = f"transcript-{channel.id}.html"

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html)

    guild_data = load(GUILDS_FILE)
    config = guild_data.get(str(channel.guild.id))

    log_channel = channel.guild.get_channel(config["logs"])
    await log_channel.send(file=discord.File(file_name))
