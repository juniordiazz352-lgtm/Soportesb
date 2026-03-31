from flask import Flask, redirect, request, session, render_template
import requests, json
import config

app = Flask(__name__)
app.secret_key = "secret"

def get_token(code):
    data = {
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config.REDIRECT_URI
    }
    r = requests.post(f"{config.API_BASE}/oauth2/token", data=data)
    return r.json()

def get_user(token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{config.API_BASE}/users/@me", headers=headers)
    return r.json()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return redirect(
        f"https://discord.com/api/oauth2/authorize?client_id={config.CLIENT_ID}&redirect_uri={config.REDIRECT_URI}&response_type=code&scope=identify"
    )

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token = get_token(code)
    user = get_user(token["access_token"])
    session["user"] = user
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    user = session["user"]

    with open("../data/tickets.json") as f:
        tickets = json.load(f)

    return render_template("dashboard.html", user=user, tickets=tickets["tickets"])

if __name__ == "__main__":
    app.run(debug=True)
