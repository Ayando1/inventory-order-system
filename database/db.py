import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "cafe.db"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_connection()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("✓ Adatbázis táblák sikeresen létrehozva.")

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM ingredients")
    if cursor.fetchone()[0] > 0:
        print("ℹ Az adatbázis már tartalmaz adatokat, seed kihagyva.")
        conn.close()
        return

    ingredients = [
        ("Kávébab", 1000.0, "g", 8.5),
        ("Tej", 5000.0, "ml", 0.45),        
        ("Zabtej", 3000.0, "ml", 0.85),       
        ("Karamell szirup", 500.0, "ml", 3.2),
    ]
    cursor.executemany(
        "INSERT INTO ingredients (name, current_stock, unit, cost_per_unit) VALUES (?, ?, ?, ?)",
        ingredients
    )

    products = [
        ("Espresso", 650),
        ("Cappuccino", 950),
        ("Karamell Latte", 1350)
    ]
    cursor.executemany(
        "INSERT INTO products (name, sale_price) VALUES (?, ?)",
        products
    )

    cursor.execute("INSERT INTO recipes VALUES (1, 1, 18.0)")
    cursor.execute("INSERT INTO recipes VALUES (2, 1, 18.0)")
    cursor.execute("INSERT INTO recipes VALUES (2, 2, 150.0)")
    cursor.execute("INSERT INTO recipes VALUES (3, 1, 18.0)")
    cursor.execute("INSERT INTO recipes VALUES (3, 2, 220.0)")
    cursor.execute("INSERT INTO recipes VALUES (3, 4, 25.0)")

    conn.commit()
    conn.close()
    print("✓ Kezdő adatok (alapanyagok, termékek, receptek) sikeresen betöltve.")

if __name__ == "__main__":
    init_db()
    seed_data()