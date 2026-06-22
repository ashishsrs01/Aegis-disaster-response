import os
import sys

import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import random

# Ensure the local workspace package is imported first, avoiding a globally installed
# package named `src` from shadowing the project's own source code.
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    import osmnx as ox
except ImportError:
    ox = None

import importlib
import src.core.environment
import src.core.victim
import src.navigation.pathfinder
import src.optimization.dispatcher
import src.reasoning.triage

importlib.reload(src.core.environment)
importlib.reload(src.core.victim)
importlib.reload(src.navigation.pathfinder)
importlib.reload(src.optimization.dispatcher)
importlib.reload(src.reasoning.triage)

from src.core.environment import CityGraph
from src.core.victim import Victim
from src.navigation.pathfinder import Pathfinder
from src.optimization.dispatcher import FleetDispatcher
from src.reasoning.triage import TriageEngine

st.set_page_config(page_title="Aegis Disaster Response", page_icon="🚑", layout="wide")

st.title("🚑 Aegis Disaster Response System")
st.markdown(
    "A college project that finds the best ambulance routes using **A* pathfinding** "
    "and **Hungarian algorithm** dispatch optimization."
)

with st.sidebar:
    st.header("Settings")

    use_osm = st.checkbox("Use Real Map (OpenStreetMap)", value=False)

    if use_osm:
        if ox is None:
            st.error("OSMnx is not installed. Run: pip install osmnx")
            st.stop()

        location_options = [
            "Piedmont, California, USA",
            "New Delhi, India",
            "Mumbai, India",
            "Bengaluru, India",
            "Custom",
        ]
        selected_location = st.selectbox("Select City / Area", location_options)

        if selected_location == "Custom":
            location_input = st.text_input(
                "Enter address or place name",
                value="Connaught Place, New Delhi, India",
                help="Use a specific address. Example: 'Marine Drive, Mumbai, India'",
            )
            use_cache = False
        else:
            location_input = selected_location
            use_cache = True

        st.caption("First load may take 10–30 seconds. Custom places use a 2 km radius.")
        grid_size = None
    else:
        grid_size = st.slider("Grid size", min_value=5, max_value=12, value=8)
        location_input = None
        selected_location = None
        use_cache = True

    run_btn = st.button("Run Simulation", type="primary", use_container_width=True)

col_results, col_map = st.columns([1, 2])

if not run_btn:
    with col_results:
        st.info("Choose your settings in the sidebar, then click **Run Simulation**.")
    with col_map:
        st.markdown("### How it works")
        st.markdown(
            """
            1. **Build a city map** — synthetic grid or real streets from OpenStreetMap  
            2. **Run A-star search** — calculate travel time from each ambulance to each victim  
            3. **Optimize dispatch** — assign ambulances to victims with minimum total time  
            4. **Show results** — routes and triage priority on the map
            """
        )
else:
    try:
        with st.spinner("Loading map and running AI modules..."):
            if use_osm:
                if not location_input or not location_input.strip():
                    st.error("Please enter a location for the custom map option.")
                    st.stop()
                city = CityGraph(location=location_input.strip(), use_cache=use_cache)
            else:
                city = CityGraph(width=grid_size, height=grid_size)

            router = Pathfinder(city)
            dispatcher = FleetDispatcher()
            triage = TriageEngine()

            nodes = list(city.graph.nodes())
            if len(nodes) < 6:
                st.error("Map is too small. Try a larger area or a different location.")
                st.stop()

            if city.is_osm:
                selected_nodes = random.sample(nodes, 6)
                ambulances = selected_nodes[:3]
                vic_nodes = selected_nodes[3:]
            else:
                ambulances = [(0, 0), (grid_size - 1, 0), (0, grid_size - 1)]
                vic_nodes = [
                    (grid_size // 2, grid_size // 2),
                    (grid_size - 2, 2),
                    (2, grid_size - 2),
                ]

            victims = [
                Victim(id=0, location=vic_nodes[0], vitals={"breathing": True, "conscious": False}),
                Victim(id=1, location=vic_nodes[1], vitals={"breathing": True, "conscious": True}),
                Victim(id=2, location=vic_nodes[2], vitals={"breathing": True, "conscious": False}),
            ]
            for v in victims:
                v.priority = triage.evaluate(v.vitals)

            cost_matrix = []
            paths = {}
            for i, amb_loc in enumerate(ambulances):
                amb_costs = []
                for j, vic in enumerate(victims):
                    path, travel_time = router.a_star(amb_loc, vic.location)
                    amb_costs.append(travel_time)
                    paths[(i, j)] = path
                cost_matrix.append(amb_costs)

            optimal_assignments = dispatcher.optimize_assignments(cost_matrix)

        with col_results:
            st.subheader("Dispatch Plan")
            if use_osm:
                st.caption(f"Map: **{location_input}** ({city.graph.number_of_nodes()} intersections)")
            else:
                st.caption(f"Map: **{grid_size}×{grid_size} grid**")

            total_time = 0
            for amb_idx, vic_idx in optimal_assignments:
                time = cost_matrix[amb_idx][vic_idx]
                priority = victims[vic_idx].priority
                if time == float("inf"):
                    st.error(f"Ambulance {amb_idx} → Victim {vic_idx} (**{priority}**) — unreachable")
                else:
                    total_time += time
                    st.success(
                        f"Ambulance {amb_idx} → Victim {vic_idx} "
                        f"(**{priority}**, ETA {time:.1f} min)"
                    )

            st.metric("Total fleet travel time", f"{total_time:.1f} min")

            st.subheader("Victim Triage (START protocol)")
            for v in victims:
                st.write(f"Victim {v.id}: **{v.priority}** — vitals: {v.vitals}")

        with col_map:
            st.subheader("Operations Map")
            st.caption("Blue squares = ambulances | Red triangles = victims | Colored lines = routes")

            if city.is_osm and ox is not None:
                routes = []
                route_colors = []
                colors = ["lime", "cyan", "yellow"]
                for amb_idx, vic_idx in optimal_assignments:
                    path = paths.get((amb_idx, vic_idx))
                    if path:
                        routes.append(path)
                        route_colors.append(colors[amb_idx % len(colors)])

                if routes:
                    fig, ax = ox.plot_graph_routes(
                        city.graph,
                        routes,
                        route_colors=route_colors,
                        route_linewidth=4,
                        node_size=0,
                        show=False,
                        close=False,
                    )
                else:
                    fig, ax = ox.plot_graph(city.graph, node_size=0, show=False, close=False)

                for amb_idx, vic_idx in optimal_assignments:
                    amb_loc = ambulances[amb_idx]
                    vic_loc = victims[vic_idx].location
                    ax.scatter(
                        city.positions[amb_loc][0],
                        city.positions[amb_loc][1],
                        c="blue",
                        marker="s",
                        s=100,
                        zorder=5,
                    )
                    ax.scatter(
                        city.positions[vic_loc][0],
                        city.positions[vic_loc][1],
                        c="red",
                        marker="^",
                        s=100,
                        zorder=5,
                    )
                st.pyplot(fig)
            else:
                fig, ax = plt.subplots(figsize=(8, 8))
                pos = city.positions
                weights = [city.graph[u][v].get("weight", 1.0) for u, v in city.graph.edges()]

                nx.draw(
                    city.graph,
                    pos,
                    ax=ax,
                    node_color="lightgray",
                    with_labels=False,
                    node_size=100,
                    edge_color=weights,
                    edge_cmap=plt.cm.Reds,
                    width=1.5,
                )

                colors = ["lime", "cyan", "yellow"]
                for amb_idx, vic_idx in optimal_assignments:
                    path = paths[(amb_idx, vic_idx)]
                    if not path:
                        continue
                    color = colors[amb_idx % len(colors)]
                    path_edges = list(zip(path, path[1:]))
                    nx.draw_networkx_nodes(
                        city.graph, pos, ax=ax, nodelist=path, node_color=color, node_size=200
                    )
                    nx.draw_networkx_edges(
                        city.graph, pos, ax=ax, edgelist=path_edges, edge_color=color, width=4
                    )
                    nx.draw_networkx_nodes(
                        city.graph,
                        pos,
                        ax=ax,
                        nodelist=[ambulances[amb_idx]],
                        node_color="blue",
                        node_shape="s",
                        node_size=400,
                    )
                    nx.draw_networkx_nodes(
                        city.graph,
                        pos,
                        ax=ax,
                        nodelist=[victims[vic_idx].location],
                        node_color="red",
                        node_shape="^",
                        node_size=400,
                    )
                st.pyplot(fig)

    except Exception as e:
        st.error(f"Could not run simulation: {e}")
        st.markdown(
            "**Tips for Custom location:** use a full address with city and country, "
            "e.g. `Marine Drive, Mumbai, India` or `Times Square, New York, USA`."
        )

st.divider()
st.caption("Aegis Disaster Response — B.Sc. Year 1 AI Project | Python · Streamlit · NetworkX · SciPy")
