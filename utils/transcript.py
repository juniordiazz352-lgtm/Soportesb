async def create_transcript(channel):
    html = "<html><body>"

    async for msg in channel.history(limit=None, oldest_first=True):
        html += f"<p><b>{msg.author}:</b> {msg.content}</p>"

    html += "</body></html>"

    file = f"{channel.name}.html"
    with open(file, "w", encoding="utf-8") as f:
        f.write(html)

    return file
