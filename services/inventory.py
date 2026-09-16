from database.db import get_connection

def get_current_stock():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, name, current_stock, unit, cost_per_unit
        FROM ingredients
        ORDER BY name ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_low_stock_alerts(threshold: float = 500.0):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT name, current_stock, unit
        FROM ingredients
        WHERE current_stock <= ?
        ORDER BY current_stock ASC
    """, (threshold,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def calculate_product_margins():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            p.id,
            p.name AS product_name,
            p.sale_price,
            ROUND(SUM(r.quantity_required * i.cost_per_unit), 2) AS unit_cost
        FROM products p
        JOIN recipes r ON p.id = r.product_id
        JOIN ingredients i ON r.ingredient_id = i.id
        GROUP BY p.id, p.name, p.sale_price
    """)
    rows = cursor.fetchall()
    conn.close()
    
    analysis = []
    for row in rows:
        item = dict(row)
        profit = item["sale_price"] - item["unit_cost"]
        margin_percent = (profit / item["sale_price"]) * 100 if item["sale_price"] else 0
        
        item["profit_per_unit"] = round(profit, 2)
        item["margin_percent"] = round(margin_percent, 1)
        analysis.append(item)
        
    return analysis

if __name__ == "__main__":
    print("--- 1. Aktuális raktárkészlet ---")
    for item in get_current_stock():
        print(f"• {item['name']}: {item['current_stock']} {item['unit']}")

    print("\n--- 2. Termékek árréselemzése (Gazdasági kimutatás) ---")
    for p in calculate_product_margins():
        print(f"• {p['product_name']}: Eladási ár: {p['sale_price']} Ft | Önköltség: {p['unit_cost']} Ft | Profit: {p['profit_per_unit']} Ft ({p['margin_percent']}%)")