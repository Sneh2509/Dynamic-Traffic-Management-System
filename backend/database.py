import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "traffic_data.db")

def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicle_counts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car INTEGER,
            bus INTEGER,
            truck INTEGER,
            bike INTEGER,
            signal_time INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_results(vehicle_counts, signal_time):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO vehicle_counts (car, bus, truck, bike, signal_time) 
        VALUES (?, ?, ?, ?, ?)
    """, (vehicle_counts["car"], vehicle_counts["bus"], vehicle_counts["truck"], vehicle_counts["bike"], signal_time))
    conn.commit()
    conn.close()

create_table()
