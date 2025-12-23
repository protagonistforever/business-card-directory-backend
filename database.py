import sqlite3
from config import DB_NAME

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        field TEXT,
        value TEXT,
        card_group INTEGER
    )''')
    conn.commit()
    conn.close()

def add_field(card_group, field, value):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO cards (field,value,card_group) VALUES (?,?,?)",(field,value,card_group))
    conn.commit()
    conn.close()

def get_cards():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT card_group,field,value FROM cards")
    data = c.fetchall()
    conn.close()
    return data

def search_cards(keyword):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        SELECT card_group, field, value
        FROM cards
        WHERE card_group IN (
            SELECT DISTINCT card_group
            FROM cards
            WHERE LOWER(field) LIKE LOWER(?)
               OR LOWER(value) LIKE LOWER(?)
        )
        ORDER BY card_group
    """, ('%' + keyword + '%', '%' + keyword + '%'))

    data = c.fetchall()
    conn.close()
    return data

def delete_card(group):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM cards WHERE card_group=?", (group,))
    conn.commit()
    conn.close()
