"""
Module: Route Optimizer
Description: Solves the transportation cost minimization problem using Linear Programming.
Standard: Senior Engineering - Prescriptive Analytics (Capstone).
"""

import pulp
import pandas as pd
import numpy as np
import logging
from typing import List, Dict, Any
from src.database import LogisticsDatabase
from src.schemas import DemandPrediction

logger = logging.getLogger(__name__)

class LogisticsOptimizer:
    def __init__(self, db_manager: LogisticsDatabase):
        self.db = db_manager

    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Simple Euclidean distance as a proxy for transport cost."""
        return np.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

    def optimize_routes(self, predictions: List[DemandPrediction]) -> Dict[str, Any]:
        """
        Finds the optimal delivery plan to minimize total cost.
        """
        try:
            # 1. Get Data
            warehouses = self.db.get_warehouses()
            customers = self.db.get_customers()
            
            # 2. Define the Problem
            prob = pulp.LpProblem("Minimize_Transport_Costs", pulp.LpMinimize)

            # 3. Decision Variables: units from warehouse i to customer j
            routes = [(w['id'], c.customer_id) for _, w in warehouses.iterrows() for c in predictions]
            route_vars = pulp.LpVariable.dicts("Route", ( [w['id'] for _, w in warehouses.iterrows()], 
                                                         [c.customer_id for c in predictions] ), 0)

            # 4. Objective Function: Sum of (Units * Distance)
            costs = []
            for _, w in warehouses.iterrows():
                for c_pred in predictions:
                    # Get customer coordinates from DB
                    cust_info = customers[customers['id'] == c_pred.customer_id].iloc[0]
                    dist = self._calculate_distance(w['lat'], w['lon'], cust_info['lat'], cust_info['lon'])
                    costs.append(route_vars[w['id']][c_pred.customer_id] * dist)
            
            prob += pulp.lpSum(costs)

            # 5. Constraints
            # Constraint A: Meet all predicted demand
            for c_pred in predictions:
                prob += pulp.lpSum([route_vars[w['id']][c_pred.customer_id] for _, w in warehouses.iterrows()]) == c_pred.predicted_demand

            # Constraint B: Do not exceed warehouse capacity
            for _, w in warehouses.iterrows():
                prob += pulp.lpSum([route_vars[w['id']][c_pred.customer_id] for c_pred in predictions]) <= w['capacity']

            # 6. Solve
            prob.solve(pulp.PULP_CBC_CMD(msg=0))

            # 7. Format Results
            results = []
            if pulp.LpStatus[prob.status] == 'Optimal':
                for _, w in warehouses.iterrows():
                    for c_pred in predictions:
                        units = route_vars[w['id']][c_pred.customer_id].varValue
                        if units > 0:
                            results.append({
                                "Warehouse": w['name'],
                                "Customer": c_pred.customer_name,
                                "Units": units
                            })
                
                return {
                    "status": "Optimal",
                    "total_cost_index": pulp.value(prob.objective),
                    "allocations": pd.DataFrame(results)
                }
            
            return {"status": "Infeasible", "allocations": pd.DataFrame()}

        except Exception as e:
            logger.error(f"Optimization failed: {e}")
            return {"status": "Error", "allocations": pd.DataFrame()}