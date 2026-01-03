import sqlite3

conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    buy_price INTEGER,
    sell_price INTEGER,
    weight REAL,
    description TEXT,
    stock INTEGER,
    buy_date TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    amount INTEGER,
    sell_date TEXT
)
""")

conn.commit()

def add_product(name, buy_price, sell_price, weight, desc, amount, buy_date):
    cursor.execute("""
    INSERT OR IGNORE INTO products
    (name, buy_price, sell_price, weight, description, stock, buy_date)
    VALUES (?, ?, ?, ?, ?, 0, ?)
    """, (name, buy_price, sell_price, weight, desc, buy_date))

    cursor.execute(
        "UPDATE products SET stock = stock + ? WHERE name = ?",
        (amount, name)
    )
    conn.commit()

def sell_product(name, amount, sell_date):
    cursor.execute("SELECT stock FROM products WHERE name=?", (name,))
    row = cursor.fetchone()
    if not row or row[0] < amount:
        return False

    cursor.execute(
        "UPDATE products SET stock = stock - ? WHERE name=?",
        (amount, name)
    )

    cursor.execute(
        "INSERT INTO sales (product, amount, sell_date) VALUES (?, ?, ?)",
        (name, amount, sell_date)
    )
    conn.commit()
    return True

def get_products():
    cursor.execute("""
    SELECT name, stock, buy_price, sell_price, weight, description
    FROM products
    """)
    return cursor.fetchall()