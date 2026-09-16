import sys
from database.db import init_db, seed_data
from services.orders import create_order, InsufficientStockError
from services.inventory import get_current_stock, get_low_stock_alerts, calculate_product_margins

def show_menu():
    print("\n" + "=" * 40)
    print("      KÁVÉZÓ KÉSZLET- ÉS RENDELÉSKEZELŐ")
    print("=" * 40)
    print("1. Aktuális raktárkészlet megtekintése")
    print("2. Alacsony készletszintek (figyelmeztetések)")
    print("3. Új rendelés leadása")
    print("4. Termékek árrés- és profitkimutatása")
    print("5. Kilépés")
    print("=" * 40)

def handle_order():
    print("\n--- Új rendelés felvétele ---")
    print("1: Espresso (650 Ft)")
    print("2: Cappuccino (950 Ft)")
    print("3: Karamell Latte (1350 Ft)")
    
    try:
        prod_id = int(input("Válassz terméket (1-3): "))
        qty = int(input("Mennyiség (db): "))
        if qty <= 0:
            print("Hibás mennyiség!")
            return
            
        create_order([{"product_id": prod_id, "quantity": qty}])
    except ValueError:
        print("Kérlek számot adj meg!")
    except InsufficientStockError as e:
        print(f"Hiba: {e}")

def main():

    init_db()
    seed_data()

    while True:
        show_menu()
        choice = input("Válassz egy menüpontot (1-5): ").strip()

        if choice == "1":
            print("\n--- Raktárkészlet ---")
            for item in get_current_stock():
                print(f"• {item['name']:<16}: {item['current_stock']:>7.1f} {item['unit']}")
        elif choice == "2":
            print("\n--- Kritikus készletek (<= 500 egység) ---")
            alerts = get_low_stock_alerts(threshold=500.0)
            if not alerts:
                print("Minden alapanyag elegendő mennyiségben áll rendelkezésre.")
            for item in alerts:
                print(f"⚠ {item['name']}: már csak {item['current_stock']} {item['unit']} maradt!")
        elif choice == "3":
            handle_order()
        elif choice == "4":
            print("\n--- Pénzügyi és Árréselemzés ---")
            for p in calculate_product_margins():
                print(f"• {p['product_name']:<15} | Ár: {p['sale_price']} Ft | Költség: {p['unit_cost']:>6.1f} Ft | Haszon: {p['margin_percent']:>5.1f}%")
        elif choice == "5":
            print("Kilépés. Viszlát!")
            sys.exit(0)
        else:
            print("Érvénytelen választás, próbáld újra.")

if __name__ == "__main__":
    main()