import os
import json
import gspread
from google.oauth2.service_account import Credentials

def get_sheet():
    creds = json.loads(os.environ["GOOGLE_CREDENTIALS"])
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = Credentials.from_service_account_info(creds, scopes=scopes)
    client = gspread.authorize(credentials)
    return client.open_by_key(os.environ["SHEET_ID"]).sheet1
