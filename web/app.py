from flask import Flask, redirect, request, session, render_template
import requests
import config

app = Flask(__name__)
app.secret_key = "secret"

API = "https://discord.com/api"

def get_user(token):
    return requests.get(f"{API}/users/@me",
        headers={"Authorization": f"Bearer {token}"}).json()

def get_guilds(token):
    return requests.get(f"{API}/users/@me/guilds",
        headers={"Authorization": f"Bearer {token}"}).json()

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login")
def login():
    return redirect(
        f"{API}/oauth2/authorize?client_id={config.CLIENT_ID}&redirect_uri={config.REDIRECT_URI}&response_type=code&scope=identify guilds"
    )

@app.route("/callback")
def callback():
    code = request.args.get("code")

    data = {
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config.REDIRECT_URI
    }

    token = requests.post(f"{API}/oauth2/token", data=data).json()
    access = token["access_token"]

    session["user"] = get_user(access)
    session["guilds"] = get_guilds(access)

    return redirect("/servers")

# 🧠 SELECTOR DE SERVIDORES
@app.route("/servers")
def servers():
    if "user" not in session:
        return redirect("/")

    return render_template("servers.html",
        user=session["user"],
        guilds=session["guilds"]
    )

# 📊 DASHBOARD POR SERVIDOR
@app.route("/dashboard/<guild_id>")
def dashboard(guild_id):
    return render_template("dashboard.html", guild_id=guild_id)

app.run(host="0.0.0.0", port=10000)
