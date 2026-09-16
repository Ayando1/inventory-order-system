import sqlite3
from database.db import get_connection

class InsufficientStockError(Exception):
    """Saját kivétel, ha nincs elegendő alapanyag a raktárban."""
    pass

def create_order(order_items: list[dict]):
    """
    Rendelés feldolgozása egyetlen atomi tranzakcióban.
    
    order_items formátuma:
    [
        {"product_id": 1, "quantity": 2},  # pl. 2 db Espresso
        {"product_id": 3, "quantity": 1}   # pl. 1 db Karamell Latte
    ]
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        required_ingredients = {}
        total_order_price = 0
        resolved_items = []

        for item in order_items:
            product_id = item["product_id"]
            qty = item["quantity"]

            cursor.execute("SELECT name, sale_price FROM products WHERE id = ?", (product_id,))
            product = cursor.fetchone()
            if not product:
                raise ValueError(f"Nem létező termék ID: {product_id}")

            unit_price = product["sale_price"]
            total_order_price += unit_price * qty
            resolved_items.append({
                "product_id": product_id,
                "quantity": qty,
                "unit_price": unit_price
            })

            cursor.execute("""
                SELECT ingredient_id, quantity_required 
                FROM recipes 
                WHERE product_id = ?
            """, (product_id,))
            recipes = cursor.fetchall()

            for recipe in recipes:
                ing_id = recipe["ingredient_id"]
                needed = recipe["quantity_required"] * qty
                required_ingredients[ing_id] = required_ingredients.get(ing_id, 0.0) + needed

        for ing_id, needed_qty in required_ingredients.items():
            cursor.execute("SELECT name, current_stock, unit FROM ingredients WHERE id = ?", (ing_id,))
            ingredient = cursor.fetchone()
            
            if ingredient["current_stock"] < needed_qty:
                raise InsufficientStockError(
                    f"Nincs elég alapanyag: '{ingredient['name']}'. "
                    f"Szükséges: {needed_qty}{ingredient['unit']}, Készlet: {ingredient['current_stock']}{ingredient['unit']}."
                )

        for ing_id, needed_qty in required_ingredients.items():
            cursor.execute("""
                UPDATE ingredients 
                SET current_stock = current_stock - ? 
                WHERE id = ?
            """, (needed_qty, ing_id))

        cursor.execute("INSERT INTO orders (total_amount) VALUES (?)", (total_order_price,))
        order_id = cursor.lastrowid

        for item in resolved_items:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, unit_price) 
                VALUES (?, ?, ?, ?)
            """, (order_id, item["product_id"], item["quantity"], item["unit_price"]))

        conn.commit()
        print(f"✓ Rendelés #{order_id} sikeresen rögzítve! Végösszeg: {total_order_price} Ft")
        return order_id

    except Exception as e:
        conn.rollback()
        print(f"✗ Rendelés megszakítva (Rollback lefutott): {e}")
        raise e

    finally:
        conn.close()


if __name__ == "__main__":
    print("--- Teszt 1: Normál rendelés (1 Espresso + 1 Karamell Latte) ---")
    try:
        create_order([
            {"product_id": 1, "quantity": 1},
            {"product_id": 3, "quantity": 1}
        ])
    except Exception:
        pass

    print("\n--- Teszt 2: Készlethiány teszt (Rendelünk 500 db Lattét) ---")
    try:
        create_order([
            {"product_id": 3, "quantity": 500}
        ])
    except InsufficientStockError:
        print("✓ A tranzakcióvédelem megfelelően elkapta a készlethiányt!")