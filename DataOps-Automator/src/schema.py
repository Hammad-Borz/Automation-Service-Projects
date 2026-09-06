"""SQLite schema definitions."""

CREATE_SALES_TABLE = """
CREATE TABLE IF NOT EXISTS sales (
    order_id TEXT PRIMARY KEY,
    order_date TEXT NOT NULL,
    customer TEXT NOT NULL,
    region TEXT NOT NULL,
    product TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price REAL NOT NULL CHECK (unit_price > 0),
    revenue REAL NOT NULL CHECK (revenue > 0),
    month TEXT NOT NULL
)
"""
