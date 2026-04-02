async def generate_transcript(channel):
    messages = [msg async for msg in channel.history(limit=None)]

    html = "<html><body>"
    html += f"<h2>Transcript - {channel.name}</h2>"

    for msg in reversed(messages):
        html += f"<p><b>{msg.author}</b>: {msg.content}</p>"

    html += "</body></html>"

    with open(f"transcript-{channel.id}.html", "w", encoding="utf-8") as f:
        f.write(html)
