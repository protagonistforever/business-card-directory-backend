import gspread
import json
import os
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]

def get_sheet():
    creds_json = json.loads(os.environ["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(creds_json, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(os.environ["SHEET_ID"]).sheet1
    return sheet

# ----------------- CRUD -----------------

def add_card(group_id, name=None, company=None, email=None,
             phone=None, date=None, products=None, custom=None):
    sheet = get_sheet()
    sheet.append_row([group_id, name, company, email, phone, date, products, custom])

def get_cards():
    sheet = get_sheet()
    rows = sheet.get_all_values()[1:]  # skip header
    return [tuple(r) for r in rows]  # returns (group_id, name, company, email, phone, date, products, custom)

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
