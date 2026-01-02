# Smart Logistics Optimizer: Capstone Project
This project is part of the Applied Data Science program, integrating descriptive, predictive, and prescriptive analytics into a unified supply chain solution. It solves a real-world transportation problem by minimizing delivery costs through mathematical optimization.

<img width="1878" height="927" alt="preview" src="https://github.com/user-attachments/assets/d7e7c800-3295-45dc-b56d-7187edb6399f" />


## 🏗️ Project Architecture
The application follows a rigorous three-phase industrial workflow:

1.  **Descriptive Phase**: Visualizes the logistics network (warehouses and customer nodes) using geographic mapping and inventory metrics.
2.  **Predictive Phase**: Implements a Linear Regression engine to forecast demand for the next business day based on historical data.
3.  **Prescriptive Phase**: Utilizes **Linear Programming (PuLP)** to solve the cost-minimization objective, determining the optimal allocation of units from hubs to customers.

## 🛠️ Tech Stack
* **Optimization**: PuLP (Linear Programming).
* **Predictive Modeling**: Scikit-Learn (Linear Regression).
* **Frontend**: Streamlit (Executive Dashboard).
* **Data Management**: SQLite & Pandas.
* **Validation**: Pydantic for schema enforcement.

## 🚀 Key Features
* **Automated Data Seeding**: Includes a `seed_data.py` script to initialize the logistics environment.
* **Mathematical Precision**: The optimizer considers warehouse capacity constraints and customer demand requirements.
* **Professional Engineering**: Full type-hinting, modular logic, and centralized configuration management.

---

## ❓ Interview FAQ (Logistics & Optimization)

**Q: Why use Linear Programming instead of a simple Greedy Algorithm?**
A: A greedy algorithm might find a local optimum by choosing the cheapest route for one customer at a time, but it often fails to minimize the global cost. Linear Programming evaluates all constraints simultaneously to find the absolute mathematical minimum.

**Q: How does the system handle a situation where demand exceeds capacity?**
A: The `route_optimizer.py` script detects "Infeasible" status. In a real-world scenario, this triggers a business alert to prioritize high-value customers or increase warehouse shifts.

**Q: How is the objective function defined in this project?**
A: The objective function is the minimization of the sum of (Units Shipped × Euclidean Distance) across all active routes, subject to supply and demand constraints.

---

📄 **License**
This project is distributed under the MIT license. Its purpose is strictly educational and research-based, developed as an Applied Data Science solution.

**Note for recruiters:**
This Capstone project demonstrates the ability to translate complex business constraints into mathematical models. It showcases mastery over the entire data lifecycle—from raw SQL data to a prescriptive engine that provides actionable strategic decisions.

Autor: JUAN S.  Contacto: https://github.com/johnyse99
