import networkx as nx
import matplotlib.pyplot as plt
import random
from typing import Tuple

class CityGraph:
    """
    Core mathematical representation of the city environment.
    Uses a 2D grid graph to simulate city blocks and intersections.
    """
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Generate a standard grid graph (like Manhattan streets)
        self.graph = nx.grid_2d_graph(width, height)
        self._initialize_edge_weights()

    def _initialize_edge_weights(self) -> None:
        """
        Assigns initial travel times (weights) to all roads.
        Currently random, but later this will be updated dynamically by the Hazard HMM.
        """
        for u, v in self.graph.edges():
            # Weight represents travel time in minutes. Normal roads take 1-3 mins.
            self.graph[u][v]['weight'] = random.uniform(1.0, 3.0)

    def get_weight(self, u: Tuple[int, int], v: Tuple[int, int]) -> float:
        """Safely retrieve the weight between two connected nodes."""
        if self.graph.has_edge(u, v):
            return self.graph[u][v]['weight']
        return float('inf') # Infinite cost if no road exists

    def visualize(self) -> None:
        """Renders the city graph for debugging and architecture verification."""
        # Map node coordinates directly to x, y positions for plotting
        pos = {(x, y): (x, y) for x, y in self.graph.nodes()}
        
        # Extract weights to color-code the roads (darker = longer travel time)
        weights = [self.graph[u][v]['weight'] for u, v in self.graph.edges()]
        
        plt.figure(figsize=(8, 8))
        nx.draw(
            self.graph, 
            pos, 
            node_color='lightblue', 
            with_labels=True, 
            node_size=600, 
            font_size=8,
            edge_color=weights, 
            edge_cmap=plt.cm.Reds, 
            width=2.5
        )
        plt.title(f"Aegis Simulator - {self.width}x{self.height} City Grid", fontsize=14)
        plt.show()

# --- Execution Block ---
# This only runs if we execute this specific file directly.
if __name__ == "__main__":
    print("Initializing City Graph...")
    city = CityGraph(width=5, height=5)
    print(f"City generated with {city.graph.number_of_nodes()} intersections and {city.graph.number_of_edges()} roads.")
    print("Opening visualization...")
    city.visualize()