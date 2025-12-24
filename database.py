import sqlite3
from config import DB_NAME


# --------------------------------------------------
# TABLE CREATION
# --------------------------------------------------

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # ONE-TIME RESET OF OLD SCHEMA
    c.execute("DROP TABLE IF EXISTS cards")

    c.execute("""
        CREATE TABLE cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_group INTEGER UNIQUE,
            name TEXT,
            company TEXT,
            email TEXT,
            phone TEXT,
            date TEXT,
            products TEXT,
            custom TEXT
        )
    """)

    conn.commit()
    conn.close()



# --------------------------------------------------
# ADD CARD (FIELDS CAN BE SKIPPED)
# --------------------------------------------------

def add_card(card_group, name=None, company=None, email=None,
             phone=None, date=None, products=None, custom=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO cards
        (card_group, name, company, email, phone, date, products, custom)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (card_group, name, company, email, phone, date, products, custom))
    conn.commit()
    conn.close()


# --------------------------------------------------
# GET ALL CARDS
# --------------------------------------------------

def get_cards():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT
            card_group, name, company, email, phone, date, products, custom
        FROM cards
        ORDER BY card_group
    """)
    data = c.fetchall()
    conn.close()
    return data


# --------------------------------------------------
# SEARCH (ANY FIELD)
# --------------------------------------------------

def search_cards(keyword):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    like = f"%{keyword.lower()}%"
    c.execute("""
        SELECT
            card_group, name, company, email, phone, date, products, custom
        FROM cards
        WHERE LOWER(name) LIKE ?
           OR LOWER(company) LIKE ?
           OR LOWER(email) LIKE ?
           OR LOWER(phone) LIKE ?
           OR LOWER(products) LIKE ?
           OR LOWER(custom) LIKE ?
        ORDER BY card_group
    """, (like, like, like, like, like, like))
    data = c.fetchall()
    conn.close()
    return data


# --------------------------------------------------
# UPDATE CARD (PARTIAL UPDATE SUPPORTED)
# --------------------------------------------------

def update_card(card_group, **fields):
    if not fields:
        return

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    updates = []
    values = []

    for key, value in fields.items():
        updates.append(f"{key}=?")
        values.append(value)

    values.append(card_group)

    query = f"""
        UPDATE cards
        SET {', '.join(updates)}
        WHERE card_group=?
    """

    c.execute(query, values)
    conn.commit()
    conn.close()


# --------------------------------------------------
# DELETE CARD
# --------------------------------------------------

def delete_card(card_group):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM cards WHERE card_group=?", (card_group,))
    conn.commit()
    conn.close()
