import sqlite3

conn = sqlite3.connect("bookings.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    trek TEXT,
    people TEXT,
    days TEXT,
    message TEXT
)
""")

conn.commit()
conn.close()

print("Database Ready ✔")

