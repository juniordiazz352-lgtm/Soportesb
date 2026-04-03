import discord
from datetime import datetime

async def generate_transcript(channel: discord.TextChannel):
    messages = []

    async for msg in channel.history(limit=None, oldest_first=True):
        time = msg.created_at.strftime("%d/%m/%Y %H:%M")

        content = msg.content or ""

        if msg.embeds:
            content += " [EMBED]"

        messages.append(f"""
        <div class="msg">
            <div class="author">{msg.author} <span>{time}</span></div>
            <div class="content">{content}</div>
        </div>
        """)

    html = f"""
    <html>
    <head>
        <style>
            body {{
                background: #0f172a;
                color: white;
                font-family: Arial;
                padding: 20px;
            }}
            .msg {{
                margin-bottom: 15px;
                padding: 10px;
                background: #1e293b;
                border-radius: 10px;
            }}
            .author {{
                font-weight: bold;
                color: #38bdf8;
            }}
            .author span {{
                font-size: 12px;
                color: #94a3b8;
                margin-left: 10px;
            }}
            .content {{
                margin-top: 5px;
            }}
        </style>
    </head>
    <body>
        <h2>Transcript - #{channel.name}</h2>
        {''.join(messages)}
    </body>
    </html>
    """

    file = discord.File(
        fp=bytes(html, "utf-8"),
        filename=f"transcript-{channel.name}.html"
    )

    return file
