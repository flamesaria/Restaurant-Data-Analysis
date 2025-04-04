import sqlite3
import pandas as pd

df = pd.read_csv("warsaw_restaurants.csv")

conn = sqlite3.connect("restaurants.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS restaurants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    rating REAL,
    review_count INTEGER,
    price TEXT,
    category TEXT,
    address TEXT,
    latitude REAL,
    longitude REAL
)
""")

df.to_sql("restaurants", conn, if_exists="replace", index=False)

cursor.execute("SELECT COUNT(*) FROM restaurants")
print("Uploaded records:", cursor.fetchone()[0])

conn.commit()
conn.close()
