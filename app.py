from flask import Flask, render_template, request, redirect, session
import config
from database import add_card, get_cards, search_cards, delete_card

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# --------------------------------------------------
# HOME – SHOW ALL CARDS
# --------------------------------------------------
@app.route("/")
def home():
    rows = get_cards()
    return render_template("search.html", cards=rows, keyword="")

# --------------------------------------------------
# SEARCH
# --------------------------------------------------
@app.route("/search")
def search():
    q = request.args.get("q", "")
    rows = search_cards(q)
    return render_template("search.html", cards=rows, keyword=q)

# --------------------------------------------------
# ADMIN LOGIN
# --------------------------------------------------
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

# --------------------------------------------------
# ADMIN DASHBOARD
# --------------------------------------------------
@app.route("/admin/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect("/admin")

    rows = get_cards()
    return render_template("admin_dashboard.html", cards=rows)

# --------------------------------------------------
# ADD CARD
# --------------------------------------------------
@app.route("/admin/add", methods=["GET", "POST"])
def add():
    if "admin" not in session:
        return redirect("/admin")

    if request.method == "POST":
        try:
            group = int(request.form.get("group_id"))
        except (TypeError, ValueError):
            return "Invalid card group", 400

        add_card(
            group_id=group,
            name=request.form.get("name") or None,
            company=request.form.get("company") or None,
            email=request.form.get("email") or None,
            phone=request.form.get("phone") or None,
            date=request.form.get("date") or None,
            products=request.form.get("products") or None,
            custom=request.form.get("custom") or None,
        )

        return redirect("/admin/dashboard")

    return render_template("add_card.html")

# --------------------------------------------------
# DELETE CARD
# --------------------------------------------------
@app.route("/admin/delete/<int:g>")
def delete(g):
    if "admin" not in session:
        return redirect("/admin")

    delete_card(g)
    return redirect("/admin/dashboard")

# --------------------------------------------------
# LOGOUT
# --------------------------------------------------
@app.route("/admin/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")

# --------------------------------------------------
# RUN APP
# --------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
