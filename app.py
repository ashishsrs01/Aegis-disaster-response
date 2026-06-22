import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import random

# Import your custom AI modules
from src.core.environment import CityGraph
from src.navigation.pathfinder import Pathfinder
from src.optimization.dispatcher import FleetDispatcher
from src.core.victim import Victim

# Configure the web page
st.set_page_config(page_title="Aegis AI System", layout="wide")

st.title("🚑 Aegis Disaster Response AI")
st.markdown("Multi-Agent Pathfinding and Fleet Optimization Dashboard")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Simulation Controls")
    
    # Toggle between Synthetic Grid and Real OSM Map
    use_osm = st.checkbox("Use Real Map (OpenStreetMap)", value=False)
    
    if use_osm:
        location_input = st.text_input("Enter City/Neighborhood", "Piedmont, California, USA")
        st.info("Note: Loading real maps can take a few seconds.")
        grid_size = None
    else:
        grid_size = st.slider("City Grid Size", min_value=5, max_value=12, value=8)
        location_input = None
        
    run_btn = st.button("🚀 Run Dispatch AI", type="primary")

if run_btn:
    with st.spinner("Initializing Environment & Calculating A* Matrices..."):
        # 1. Initialize core AI systems
        if use_osm:
            city = CityGraph(location=location_input)
        else:
            city = CityGraph(width=grid_size, height=grid_size)
            
        router = Pathfinder(city)
        dispatcher = FleetDispatcher()
        
        # 2. Define entities dynamically
        nodes = list(city.graph.nodes())
        
        if city.is_osm:
            # Pick random real intersections for ambulances and victims
            selected_nodes = random.sample(nodes, 6)
            ambulances = selected_nodes[:3]
            vic_nodes = selected_nodes[3:]
        else:
            # Use deterministic grid positions
            ambulances = [(0, 0), (grid_size-1, 0), (0, grid_size-1)]
            vic_nodes = [
                (grid_size//2, grid_size//2),
                (grid_size-2, 2),
                (2, grid_size-2)
            ]
            
        victims = [
            Victim(id=0, location=vic_nodes[0], vitals={'breathing': True, 'conscious': False}),
            Victim(id=1, location=vic_nodes[1], vitals={'breathing': True, 'conscious': True}),
            Victim(id=2, location=vic_nodes[2], vitals={'breathing': True, 'conscious': False})
        ]
        
        # 3. Build the A* Cost Matrix
        cost_matrix = []
        paths = {}
        for i, amb_loc in enumerate(ambulances):
            amb_costs = []
            for j, vic in enumerate(victims):
                path, travel_time = router.a_star(amb_loc, vic.location)
                amb_costs.append(travel_time)
                paths[(i, j)] = path
            cost_matrix.append(amb_costs)
            
        # 4. Run the Operations Research Optimizer
        optimal_assignments = dispatcher.optimize_assignments(cost_matrix)
        
        # 5. Display Text Results
        with col1:
            st.subheader("Optimal Dispatch Strategy")
            total_time = 0
            for amb_idx, vic_idx in optimal_assignments:
                time = cost_matrix[amb_idx][vic_idx]
                total_time += time
                st.success(f"🚑 Amb {amb_idx} ➔ 🧍 Victim {vic_idx} (ETA: {time:.2f} mins)")
            st.info(f"**Total Fleet Time:** {total_time:.2f} mins")
        
        # 6. Render the Map visually
        with col2:
            st.subheader("Live Operations Map")
            fig, ax = plt.subplots(figsize=(8, 8))
            
            # Use cached positions from environment
            pos = city.positions
            weights = [city.graph[u][v].get('weight', 1.0) for u, v in city.graph.edges()]
            
            nx.draw(city.graph, pos, ax=ax, node_color='lightgray', with_labels=False, 
                    node_size=10 if city.is_osm else 100, 
                    edge_color=weights, edge_cmap=plt.cm.Reds, 
                    width=0.5 if city.is_osm else 1.5)
            
            colors = ['lime', 'cyan', 'yellow']
            for amb_idx, vic_idx in optimal_assignments:
                path = paths[(amb_idx, vic_idx)]
                if not path:
                    continue
                color = colors[amb_idx % len(colors)]
                
                path_edges = list(zip(path, path[1:]))
                nx.draw_networkx_nodes(city.graph, pos, ax=ax, nodelist=path, node_color=color, node_size=30 if city.is_osm else 200)
                nx.draw_networkx_edges(city.graph, pos, ax=ax, edgelist=path_edges, edge_color=color, width=2 if city.is_osm else 4)
                
                nx.draw_networkx_nodes(city.graph, pos, ax=ax, nodelist=[ambulances[amb_idx]], node_color='blue', node_shape='s', node_size=100 if city.is_osm else 400)
                nx.draw_networkx_nodes(city.graph, pos, ax=ax, nodelist=[victims[vic_idx].location], node_color='red', node_shape='^', node_size=100 if city.is_osm else 400)
                
            st.pyplot(fig)