import networkx as nx
import matplotlib.pyplot as plt
import random
from typing import Tuple, List, Union, Any

# Optional import for real-world maps
try:
    import osmnx as ox
except ImportError:
    ox = None

class CityGraph:
    """
    Core mathematical representation of the city environment.
    Supports both synthetic 2D grids and real-world OSM data.
    """
    def __init__(self, width: int = None, height: int = None, location: str = None, filepath: str = None):
        """
        Creates either a synthetic grid graph or loads a real OpenStreetMap network.
        """
        if location and ox:
            print(f"Loading real OSM data for '{location}'...")
            # Fetch the drive network for the specified location
            self.graph = ox.graph_from_place(location, network_type='drive')
            self.is_osm = True
            
        elif filepath and ox:
            print(f"Loading OSM data from file {filepath}...")
            self.graph = ox.load_graphml(filepath)
            self.is_osm = True
            
        else:
            print("Generating synthetic grid graph...")
            self.width = width or 10
            self.height = height or 10
            self.graph = nx.grid_2d_graph(self.width, self.height)
            self.is_osm = False
            
        self._cache_node_positions()
        self._initialize_edge_weights()

    def _cache_node_positions(self) -> None:
        """Cache coordinates for distance calculations and rendering."""
        self.positions = {}
        for node in self.graph.nodes():
            if self.is_osm:
                # OSM graphs store coordinates in 'x' (longitude) and 'y' (latitude) attributes
                self.positions[node] = (self.graph.nodes[node]['x'], self.graph.nodes[node]['y'])
            else:
                # Synthetic grid graphs use the node ID tuple (x, y) as the position
                self.positions[node] = node

    def _initialize_edge_weights(self) -> None:
        """Assigns initial travel times (weights) to all roads."""
        if self.is_osm:
            for u, v, key, data in self.graph.edges(keys=True, data=True):
                if 'length' in data:
                    data['weight'] = data['length'] / 500.0
                else:
                    data['weight'] = 1.0
        else:
            for u, v in self.graph.edges():
                self.graph[u][v]['weight'] = random.uniform(1.0, 3.0)

    def get_weight(self, u: Any, v: Any) -> float:
        """Safely retrieve the weight between two connected nodes."""
        if self.graph.has_edge(u, v):
            if self.is_osm:
                return min(data.get('weight', float('inf')) for data in self.graph[u][v].values())
            return self.graph[u][v]['weight']
        return float('inf') # Infinite cost if no road exists

    def get_node_coords(self, node: Any) -> Tuple[float, float]:
        """Returns the (x, y) or (lon, lat) coordinates of a node."""
        return self.positions.get(node, (0, 0))

    def visualize(self, path: List[Any] = None) -> None:
        """Renders the city graph and optionally overlays a calculated path."""
        pos = self.positions
        weights = [self.graph[u][v].get('weight', 1.0) for u, v in self.graph.edges()]
        
        plt.figure(figsize=(10, 10))
        
        # Draw base graph
        nx.draw(
            self.graph, pos, node_color='lightblue', with_labels=not self.is_osm, 
            node_size=50 if self.is_osm else 600, font_size=8, 
            edge_color=weights, edge_cmap=plt.cm.Reds, width=2.0
        )
        
        # If a path was provided, draw it in bright green on top
        if path:
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_nodes(self.graph, pos, nodelist=path, node_color='lime', node_size=100 if self.is_osm else 700)
            nx.draw_networkx_edges(self.graph, pos, edgelist=path_edges, edge_color='lime', width=4)
            
        title = "OSM Route Visualization" if self.is_osm else "Synthetic Grid Visualization"
        plt.title(f"Aegis Simulator - {title}", fontsize=14)
        plt.show()

    def update_hazard_level(self, u: Any, v: Any, probability: float) -> None:
        """
        Updates the weight of a road based on the probability of a hazard.
        """
        if not self.graph.has_edge(u, v):
            return

        if probability > 0.6:
            new_weight = 999.0  # Impassable
        elif probability > 0.2:
            new_weight = 10.0   # Dangerous/Slow
        else:
            new_weight = 1.0    # Clear

        if self.is_osm:
            for key in self.graph[u][v]:
                self.graph[u][v][key]['weight'] = new_weight
        else:
            self.graph[u][v]['weight'] = new_weight
        print(f"Road {u}->{v} weight updated to {new_weight} (Prob: {probability:.2f})")

# --- Execution Block ---
if __name__ == "__main__":
    print("Initializing City Graph...")
    city = CityGraph(width=5, height=5)
    print(f"City generated with {city.graph.number_of_nodes()} intersections.")
    city.visualize()