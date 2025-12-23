from flask import Flask, render_template, request, redirect, session
import config
from database import *

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

create_tables()

@app.route("/")
def home():
    rows = get_cards()
    cards = {}
    for g, f, v in rows:
        cards.setdefault(g, {})[f] = v
    return render_template("search.html", cards=cards, keyword="")

@app.route("/search")
def search():
    q = request.args.get("q", "")
    rows = search_cards(q)
    cards = {}
    for g, f, v in rows:
        cards.setdefault(g, {})[f] = v
    return render_template("search.html", cards=cards, keyword=q)

@app.route("/admin")
def admin():
    return render_template("admin_login.html")

@app.route("/admin/auth", methods=["POST"])
def auth():
    if (
        request.form["username"] == config.ADMIN_USERNAME
        and request.form["password"] == config.ADMIN_PASSWORD
    ):
        session["admin"] = True
        return redirect("/admin/dashboard")
    return "Invalid Login", 401

@app.route("/admin/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect("/admin")

    rows = get_cards()
    cards = {}
    for g, f, v in rows:
        cards.setdefault(g, {})[f] = v

    return render_template("admin_dashboard.html", cards=cards)

@app.route("/admin/add", methods=["GET", "POST"])
def add():
    if "admin" not in session:
        return redirect("/admin")

    if request.method == "POST":
        add_field(
            int(request.form["group"]),
            request.form["field"],
            request.form["value"],
        )
        return redirect("/admin/dashboard")

    return render_template("add_card.html")

@app.route("/admin/delete/<int:g>")
def delete(g):
    if "admin" not in session:
        return redirect("/admin")
    delete_card(g)
    return redirect("/admin/dashboard")

@app.route("/admin/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")

if __name__ == "__main__":
    app.run()
