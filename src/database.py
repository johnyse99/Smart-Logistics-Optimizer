"""
Module: Database Manager
Description: Handles all SQL operations for the Logistics Capstone Project.
Inputs: SQL Queries to logistics.db.
Outputs: DataFrames for descriptive and predictive analysis.
"""

import sqlite3
import pandas as pd
import logging
from typing import Optional
from src.config import config

# Senior logging standard
logger = logging.getLogger(__name__)

class LogisticsDatabase:
    def __init__(self, db_path: str = config.DB_PATH):
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        """Establishes and returns a database connection."""
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise

    def get_warehouses(self) -> pd.DataFrame:
        """Retrieves all warehouse data for descriptive mapping."""
        query = "SELECT * FROM warehouses"
        try:
            with self._get_connection() as conn:
                return pd.read_sql_query(query, conn)
        except Exception as e:
            logger.error(f"Error fetching warehouses: {e}")
            return pd.DataFrame()

    def get_customers(self) -> pd.DataFrame:
        """Retrieves all customer location data."""
        query = "SELECT * FROM customers"
        try:
            with self._get_connection() as conn:
                return pd.read_sql_query(query, conn)
        except Exception as e:
            logger.error(f"Error fetching customers: {e}")
            return pd.DataFrame()

    def get_historical_demand(self) -> pd.DataFrame:
        """Retrieves demand history for the predictive model."""
        query = """
            SELECT d.day, d.units_requested, c.name as customer_name, c.id as customer_id
            FROM historical_demand d
            JOIN customers c ON d.customer_id = c.id
        """
        try:
            with self._get_connection() as conn:
                return pd.read_sql_query(query, conn)
        except Exception as e:
            logger.error(f"Error fetching demand data: {e}")
            return pd.DataFrame()

    def get_total_capacity(self) -> int:
        """Calculates total network capacity across all warehouses."""
        query = "SELECT SUM(capacity) FROM warehouses"
        try:
            with self._get_connection() as conn:
                result = conn.execute(query).fetchone()
                return result[0] if result[0] else 0
        except Exception as e:
            logger.error(f"Error calculating total capacity: {e}")
            return 0