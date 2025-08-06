import sqlite3

# Absolute path to the database file (use double backslashes or raw string)
db_path = r"C:\Users\<YOUR USER NAME>\Documents\customers.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
''')

cursor.execute("INSERT OR IGNORE INTO customers (id, name) VALUES (?, ?)", (123, 'John Doe'))
cursor.execute("INSERT OR IGNORE INTO customers (id, name) VALUES (?, ?)", (456, 'Jane Smith'))

conn.commit()
conn.close()

print(f"Database created at {db_path} with sample data.")
