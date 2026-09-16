# ☕ Cafe Inventory & Order Management System

A transactional inventory and order processing engine designed to model real-world business logic for retail food & beverage operations. Built with Python and SQLite, the system ensures data consistency through ACID transactions, automatic ingredient stock deductions, and financial margin analysis.

---

## 🚀 Key Features

* **Atomic Order Processing:** Utilizes database transactions (`BEGIN`, `COMMIT`, `ROLLBACK`) to guarantee that ingredients are deducted only if sufficient stock exists across all recipe components.
* **Relational Recipe Mapping:** Implements many-to-many (`N:M`) mapping between finished products and raw ingredients with unit conversions.
* **Financial & Margin Reporting:** Calculates real-time unit costs, gross margins, and profit percentages per menu item using multi-table SQL queries.
* **Low-Stock Alerts:** Identifies critical inventory levels to assist procurement and supply chain decisions.

---

## 🛠️ Tech Stack & Concepts

* **Language:** Python 3.10+
* **Database:** SQLite3
* **Database Architecture:** Relational schemas, Foreign Keys (`ON DELETE CASCADE`), Indexes, Transaction Control
* **Concepts:** ACID Principles, Data Integrity, CLI Interface, Modular Architecture

---

## 📂 Project Structure

```text
inventory-order-system/
│
├── database/
│   ├── db.py          # Database initialization & connection pooling
│   └── schema.sql     # DDL definitions (tables, constraints, relationships)
│
├── services/
│   ├── inventory.py   # Stock alerts & margin analytics
│   └── orders.py      # Transactional order placement & validation
│
├── main.py            # Interactive CLI application entry point
├── .gitignore         # Ignores byte-code and generated database files
└── README.md          # Technical documentation
