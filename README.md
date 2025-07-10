## 📝 Description
This project is a DSA-heavy simulation of an intelligent, automated warehouse system inspired by real-world operations like Amazon Robotics.
It models a dynamic grid warehouse, where autonomous robots pick and move inventory items efficiently while avoiding conflicts and optimizing paths in real time.

## 🚀 Tech Stack
Backend & Core Logic: Python 3.10+ with custom Data Structures & Algorithms (Grid Graph, A*, DSU, Segment Tree, PQ).

Frontend: Streamlit and Flask for real-time dashboards and visualizations,HTML CSS for GUI.

Database: SQLite for persisting orders, robots, and inventory states.

## ⚡ Key Features
	•	🕸️ Dynamic Warehouse Graph — Cells can be blocked/unblocked to simulate moving shelves.
	•	🚦 A* Pathfinding — Fast, heuristic-based robot route planning.
	•	⚔️ Conflict Resolver — Reservation Table + Priority Queue for collision avoidance.
	•	🔗 Union-Find Logic — Manage robot fleet groups or merge/split warehouse zones.
	•	📈 Segment Tree — Range sum queries for hot-zone inventory tracking.
	•	📦 Order Priority Manager — Rank tasks based on urgency and deadlines.
	•	🗃️ Optional SQLite DB — Persist orders, robot states, and logs.
	•	📊 Optional Dashboards — Visualize robot paths and warehouse status in real time.

## 🔑 Core goals:
	•	Model the warehouse layout as a dynamic 2D/3D grid graph.
	•	Use A* search for real-time robot path planning.
	•	Implement a reservation system (Conflict Resolver) to avoid robot collisions and deadlocks.
	•	Use Disjoint Set Union (DSU) for managing robot fleets and zone merging.
	•	Use Segment Tree or Fenwick Tree to track and query inventory across zones.
	•	Prioritize orders dynamically with a Priority Queue, ensuring urgent tasks are handled first.
	•	(Optional) Use SQLite for persistent storage of orders, robots, inventory levels, and event logs.
	•	(Optional) Add dashboards to visualize robot movements, paths, and warehouse state.
 
