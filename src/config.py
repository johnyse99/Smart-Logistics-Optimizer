"""
Module: Configuration Manager
Description: Defines global constants and paths for the Logistics project.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Project Info
    APP_TITLE = "Smart Logistics Optimizer"
    
    # Paths
    # Relative path to the logistics database
    DB_PATH = os.getenv("DB_PATH", "data/logistics.db")
    
    # Business Logic Constants
    FUEL_COST_PER_KM = 1.50  # Default value in USD
    MAX_TRUCK_CAPACITY = 500 # Units per vehicle

config = Config()