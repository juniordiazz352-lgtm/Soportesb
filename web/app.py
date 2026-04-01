from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# 📂 CARPETA TRANSCRIPTS
TRANSCRIPTS_FOLDER = "web/transcripts"

@app.route("/")
def home():
    files = os.listdir(TRANSCRIPTS_FOLDER)
    return render_template("transcripts.html", files=files)

# 📄 VER TRANSCRIPT
@app.route("/transcript/<name>")
def transcript(name):
    return send_from_directory(TRANSCRIPTS_FOLDER, name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
