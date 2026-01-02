"""
Utility Script: Logistics Data Generator
Description: Creates the SQLite database for the Capstone Project.
Standards: Senior Data Engineering - Automated Setup.
"""

import sqlite3
import pandas as pd
import os
import logging
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_logistics_db():
    db_path = 'data/logistics.db'
    os.makedirs('data', exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 1. Warehouses Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS warehouses (
            id INTEGER PRIMARY KEY,
            name TEXT,
            lat REAL,
            lon REAL,
            capacity INTEGER
        )''')

        warehouses = [
            (1, 'Central Hub', 40.7128, -74.0060, 5000),
            (2, 'North Branch', 40.7831, -73.9712, 3000),
            (3, 'South Port', 40.6782, -73.9442, 4000)
        ]
        cursor.executemany('INSERT OR REPLACE INTO warehouses VALUES (?,?,?,?,?)', warehouses)

        # 2. Customers Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            lat REAL,
            lon REAL
        )''')

        customers = [
            (101, 'Retail Store A', 40.7580, -73.9855),
            (102, 'Pharmacy B', 40.7484, -73.9857),
            (103, 'Supermarket C', 40.7306, -73.9352),
            (104, 'Tech Shop D', 40.7061, -74.0092),
            (105, 'Hospital E', 40.8075, -73.9626)
        ]
        cursor.executemany('INSERT OR REPLACE INTO customers VALUES (?,?,?,?)', customers)

        # 3. Historical Demand Table (For Predictive Phase)
        # Generamos demanda aleatoria para los últimos 30 días
        demand_records = []
        for day in range(1, 31):
            for cust_id in [101, 102, 103, 104, 105]:
                demand = np.random.randint(50, 200)
                demand_records.append((day, cust_id, demand))
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS historical_demand (
            day INTEGER,
            customer_id INTEGER,
            units_requested INTEGER
        )''')
        cursor.executemany('INSERT INTO historical_demand VALUES (?,?,?)', demand_records)

        conn.commit()
        logger.info(f"Database successfully initialized at {db_path}")

    except Exception as e:
        logger.error(f"Failed to seed database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_logistics_db()