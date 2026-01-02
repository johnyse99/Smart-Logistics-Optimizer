"""
Main Application - Smart Logistics Optimizer
Standard: Senior AI Engineering (Capstone Project)
"""

import streamlit as st
import pandas as pd
import logging
from src.config import config
from src.database import LogisticsDatabase
from src.demand_predictor import DemandForecaster
from src.route_optimizer import LogisticsOptimizer

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

def main():
    st.set_page_config(page_title=config.APP_TITLE, page_icon="🚚", layout="wide")
    db = LogisticsDatabase()
    forecaster = DemandForecaster(db)
    optimizer = LogisticsOptimizer(db)

    st.sidebar.title("Capstone Logistics")
    phase = st.sidebar.radio("Select Phase:", ["📊 Descriptive", "🤖 Predictive", "🎯 Prescriptive"])
    st.title(f"🚚 {config.APP_TITLE}")
    st.divider()

    # --- PHASE 1: DESCRIPTIVE ---
    if phase == "📊 Descriptive":
        st.header("Supply Chain Network Overview")
        df_w = db.get_warehouses()
        df_c = db.get_customers()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Capacity", f"{db.get_total_capacity()} Units")
        m2.metric("Warehouses", len(df_w))
        m3.metric("Customer Nodes", len(df_c))

        st.subheader("Network Distribution")
        st.map(pd.concat([df_w[['lat', 'lon']], df_c[['lat', 'lon']]]))

    # --- PHASE 2: PREDICTIVE ---
    elif phase == "🤖 Predictive":
        st.header("Demand Forecasting (Day 31)")
        if st.button("🚀 Run Forecast Model"):
            with st.spinner("Analyzing trends..."):
                predictions = forecaster.forecast_next_day(31)
                st.session_state.current_predictions = predictions
                st.success("Forecast completed!")

        if 'current_predictions' in st.session_state:
            df_p = pd.DataFrame([{"Customer": p.customer_name, "Units": p.predicted_demand} for p in st.session_state.current_predictions])
            st.bar_chart(df_p.set_index("Customer"))
            st.dataframe(df_p, use_container_width=True)

    # --- PHASE 3: PRESCRIPTIVE ---
    elif phase == "🎯 Prescriptive":
        st.header("Strategic Route Optimization")
        
        if 'current_predictions' not in st.session_state:
            st.warning("⚠️ Please run the 'Predictive Phase' first.")
        else:
            if st.button("⚖️ Calculate Optimal Logistics Plan"):
                with st.spinner("Solving mathematical model..."):
                    results = optimizer.optimize_routes(st.session_state.current_predictions)
                    
                    if results['status'] == "Optimal":
                        st.balloons()
                        st.success(f"Optimal Plan Found! Efficiency Score: {results['total_cost_index']:.2f}")
                        
                        st.subheader("Distribution Plan")
                        st.dataframe(results['allocations'], use_container_width=True, hide_index=True)
                        
                        # Resumen por Almacén
                        st.subheader("Warehouse Load Summary")
                        summary = results['allocations'].groupby("Warehouse")["Units"].sum()
                        st.bar_chart(summary)
                    else:
                        st.error("Model Infeasible: Demand exceeds total capacity.")

if __name__ == "__main__":
    main()