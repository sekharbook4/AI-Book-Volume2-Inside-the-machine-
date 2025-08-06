import sqlite3
import os

# Absolute path for your DB file
DB_PATH = r"C:/Users/<Your user Name>/Documents/customer_data.db"

# Make sure the folder exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Connect (this will create the file if it doesn't exist)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create a table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
)
''')

# Insert example data (ignore if already exists)
cursor.execute("INSERT OR IGNORE INTO customers VALUES (?, ?, ?)", ("123", "Alice", "alice@example.com"))
cursor.execute("INSERT OR IGNORE INTO customers VALUES (?, ?, ?)", ("456", "Bob", "bob@example.com"))

conn.commit()
conn.close()

print(f"Database created (or opened) at {DB_PATH}")
