from flask import Flask, render_template, request, redirect, session
import config
import gspread
import os
import json
from google.oauth2.service_account import Credentials

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# -------------------- Google Sheets Setup --------------------
SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]

def get_sheet():
    creds_json = json.loads(os.environ["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(creds_json, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(os.environ["SHEET_ID"]).sheet1
    return sheet

# -------------------- CRUD Operations --------------------
def add_card(group_id, name=None, company=None, email=None,
             phone=None, date=None, products=None, custom=None):
    sheet = get_sheet()
    sheet.append_row([group_id, name, company, email, phone, date, products, custom])

def get_cards():
    sheet = get_sheet()
    rows = sheet.get_all_values()[1:]  # skip header
    return [tuple(r) for r in rows]

def search_cards(keyword):
    sheet = get_sheet()
    rows = sheet.get_all_values()[1:]
    keyword = keyword.lower()
    result = []
    for r in rows:
        if any(keyword in (cell or '').lower() for cell in r):
            result.append(tuple(r))
    return result

def delete_card(group_id):
    sheet = get_sheet()
    rows = sheet.get_all_values()
    for i in range(len(rows) - 1, 0, -1):  # iterate backwards
        if rows[i][0] == str(group_id):
            sheet.delete_rows(i + 1)

# -------------------- Routes --------------------
@app.route("/")
def home():
    cards = get_cards()
    return render_template("search.html", cards=cards, keyword="")

@app.route("/search")
def search():
    q = request.args.get("q", "")
    cards = search_cards(q)
    return render_template("search.html", cards=cards, keyword=q)

@app.route("/admin")
def admin():
    return render_template("admin_login.html")

@app.route("/admin/auth", methods=["POST"])
def auth():
    if request.form["username"] == config.ADMIN_USERNAME and request.form["password"] == config.ADMIN_PASSWORD:
        session["admin"] = True
        return redirect("/admin/dashboard")
    return "Invalid Login", 401

@app.route("/admin/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect("/admin")
    cards = get_cards()
    return render_template("admin_dashboard.html", cards=cards)

@app.route("/admin/add", methods=["GET", "POST"])
def add():
    if "admin" not in session:
        return redirect("/admin")

    if request.method == "POST":
        group_raw = request.form.get("group_id")
        if not group_raw or not group_raw.strip():
            return "Invalid card group", 400

        try:
            group = int(group_raw)
        except ValueError:
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

# -------------------- Run --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
