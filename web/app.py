from flask import Flask, redirect, request, session, render_template
import requests, json
import config

app = Flask(__name__)
app.secret_key = "secret"

def load(path):
    with open(path, "r") as f:
        return json.load(f)

def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# 🔐 LOGIN
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

    data = {
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config.REDIRECT_URI
    }

    token = requests.post("https://discord.com/api/oauth2/token", data=data).json()
    user = requests.get(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bearer {token['access_token']}"}
    ).json()

    session["user"] = user
    return redirect("/dashboard")

# 📊 DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    tickets = load("../data/tickets.json")
    stats = load("../data/stats.json")

    return render_template(
        "dashboard.html",
        user=session["user"],
        tickets=tickets["tickets"],
        stats=stats
    )

# 🎫 CREAR TICKET DESDE WEB
@app.route("/create_ticket", methods=["GET", "POST"])
def create_ticket():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        nombre = request.form["nombre"]
        titulo = request.form["titulo"]
        descripcion = request.form["descripcion"]
        emoji = request.form["emoji"]

        data = load("../data/tickets.json")

        data["tickets"][nombre] = {
            "titulo": titulo,
            "descripcion": descripcion,
            "emoji": emoji
        }

        save("../data/tickets.json", data)

        return redirect("/dashboard")

    return render_template("create_ticket.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
