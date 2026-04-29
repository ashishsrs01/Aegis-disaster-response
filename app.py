import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

# Import your custom AI modules
from src.core.environment import CityGraph
from src.navigation.pathfinder import Pathfinder
from src.optimization.dispatcher import FleetDispatcher
from src.core.victim import Victim

# Configure the web page
st.set_page_config(page_title="Aegis AI System", layout="wide")

st.title("🚑 Aegis Disaster Response AI")
st.markdown("Multi-Agent Pathfinding and Fleet Optimization Dashboard")

# Create a UI layout with two columns (1/3 width and 2/3 width)
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Simulation Controls")
    # Add an interactive slider to change the city size
    grid_size = st.slider("City Grid Size", min_value=5, max_value=12, value=8)
    
    # Add a button to trigger the AI
    run_btn = st.button("🚀 Run Dispatch AI", type="primary")

# This block only runs when the user clicks the button
if run_btn:
    with st.spinner("Initializing Environment & Calculating A* Matrices..."):
        # 1. Initialize core AI systems
        city = CityGraph(width=grid_size, height=grid_size)
        router = Pathfinder(city)
        dispatcher = FleetDispatcher()
        
        # 2. Define entities dynamically based on grid size
        ambulances = [(0, 0), (grid_size-1, 0), (0, grid_size-1)]
        victims = [
            Victim(id=0, location=(grid_size//2, grid_size//2), vitals={'breathing': True, 'conscious': False}),
            Victim(id=1, location=(grid_size-2, 2), vitals={'breathing': True, 'conscious': True}),
            Victim(id=2, location=(2, grid_size-2), vitals={'breathing': True, 'conscious': False})
        ]
        
        # 3. Build the A* Cost Matrix
        cost_matrix = []
        paths = {} # Store the paths so we can draw them later
        for i, amb_loc in enumerate(ambulances):
            amb_costs = []
            for j, vic in enumerate(victims):
                path, travel_time = router.a_star(amb_loc, vic.location)
                amb_costs.append(travel_time)
                paths[(i, j)] = path
            cost_matrix.append(amb_costs)
            
        # 4. Run the Operations Research Optimizer
        optimal_assignments = dispatcher.optimize_assignments(cost_matrix)
        
        # 5. Display Text Results in the left column
        with col1:
            st.subheader("Optimal Dispatch Strategy")
            total_time = 0
            for amb_idx, vic_idx in optimal_assignments:
                time = cost_matrix[amb_idx][vic_idx]
                total_time += time
                # UI success message
                st.success(f"🚑 Amb {amb_idx} ➔ 🧍 Victim {vic_idx} (ETA: {time:.2f} mins)")
            
            st.info(f"**Total Fleet Time:** {total_time:.2f} mins")
        
        # 6. Render the Map visually in the right column
        with col2:
            st.subheader("Live Operations Map")
            
            # Setup Matplotlib for Streamlit
            fig, ax = plt.subplots(figsize=(8, 8))
            pos = {(x, y): (x, y) for x, y in city.graph.nodes()}
            weights = [city.graph[u][v]['weight'] for u, v in city.graph.edges()]
            
            # Draw the base city roads
            nx.draw(city.graph, pos, ax=ax, node_color='lightgray', with_labels=False, 
                    node_size=100, edge_color=weights, edge_cmap=plt.cm.Reds, width=1.5)
            
            # Draw the optimal paths for each assigned pair
            colors = ['lime', 'cyan', 'yellow']
            for amb_idx, vic_idx in optimal_assignments:
                path = paths[(amb_idx, vic_idx)]
                color = colors[amb_idx % len(colors)]
                
                # Draw the specific route
                path_edges = list(zip(path, path[1:]))
                nx.draw_networkx_nodes(city.graph, pos, ax=ax, nodelist=path, node_color=color, node_size=200)
                nx.draw_networkx_edges(city.graph, pos, ax=ax, edgelist=path_edges, edge_color=color, width=4)
                
                # Mark Ambulances (Blue Squares) and Victims (Red Triangles)
                nx.draw_networkx_nodes(city.graph, pos, ax=ax, nodelist=[ambulances[amb_idx]], node_color='blue', node_shape='s', node_size=400)
                nx.draw_networkx_nodes(city.graph, pos, ax=ax, nodelist=[victims[vic_idx].location], node_color='red', node_shape='^', node_size=400)
                
            # Send the figure to the Streamlit UI
            st.pyplot(fig)