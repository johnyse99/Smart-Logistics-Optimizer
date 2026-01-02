"""
Module: Demand Predictor
Description: Uses Linear Regression to forecast demand for the next business day.
Standard: Senior AI Engineering (Type hints, Error handling, SOLID).
"""

import pandas as pd
import numpy as np
import logging
from typing import List
from sklearn.linear_model import LinearRegression
from src.database import LogisticsDatabase
from src.schemas import DemandPrediction

logger = logging.getLogger(__name__)

class DemandForecaster:
    def __init__(self, db_manager: LogisticsDatabase):
        self.db = db_manager
        self.model = LinearRegression()

    def forecast_next_day(self, target_day: int = 31) -> List[DemandPrediction]:
        """
        Trains a model per customer to predict their next day demand.
        """
        predictions = []
        try:
            df = self.db.get_historical_demand()
            if df.empty:
                logger.warning("No historical data found to train.")
                return []

            customer_ids = df['customer_id'].unique()

            for c_id in customer_ids:
                # Filter data for specific customer
                cust_data = df[df['customer_id'] == c_id].sort_values('day')
                cust_name = cust_data['customer_name'].iloc[0]

                # Prepare features (X = Day, y = Units)
                X = cust_data[['day']].values
                y = cust_data['units_requested'].values

                # Train a simple regression model
                self.model.fit(X, y)
                
                # Predict for target_day
                prediction_val = self.model.predict([[target_day]])[0]
                
                # Ensure no negative demand and round
                final_demand = max(0, round(float(prediction_val), 2))

                predictions.append(DemandPrediction(
                    customer_id=c_id,
                    customer_name=cust_name,
                    predicted_demand=final_demand
                ))

            logger.info(f"Forecast for day {target_day} completed successfully.")
            return predictions

        except Exception as e:
            logger.error(f"Error during demand forecasting: {e}")
            return []