import heapq
from typing import List, Tuple, Dict, Any
from src.core.environment import CityGraph

class Pathfinder:
    """
    Handles routing for agents through the city graph.
    """
    def __init__(self, city: CityGraph):
        self.city = city

    def heuristic(self, a: Any, b: Any) -> float:
        """
        The heuristic function h(n). Calculates distance.
        Uses cached node coordinates from the environment.
        """
        x1, y1 = self.city.get_node_coords(a)
        x2, y2 = self.city.get_node_coords(b)
        
        if self.city.is_osm:
            # For OSM (lat/lon), a simple geographic multiplier works roughly 
            # for short distances to guide A* towards the goal.
            return (abs(x1 - x2) + abs(y1 - y2)) * 100.0
        else:
            # Manhattan distance for grid
            return abs(x1 - x2) + abs(y1 - y2)

    def a_star(self, start: Any, goal: Any) -> Tuple[List[Any], float]:
        """
        A* Search Algorithm. 
        Finds the fastest path considering road weights (traffic/hazards).
        """
        # Priority Queue: Always pops the node with the lowest f_score
        frontier = []
        # In case of tie-breaking in heap, we can't compare nodes if they are tuples vs ints.
        # So we add a tiebreaker counter.
        counter = 0
        heapq.heappush(frontier, (0, counter, start))
        
        # Keep track of where we came from to reconstruct the final route
        came_from: Dict[Any, Any] = {}
        
        # g_score: Actual travel time from start to a specific node
        g_score = {node: float('inf') for node in self.city.graph.nodes()}
        if start in g_score:
            g_score[start] = 0
        else:
            return [], float('inf')
        
        while frontier:
            current_f, _, current_node = heapq.heappop(frontier)
            
            # If we reached the victim, trace our steps back to get the path
            if current_node == goal:
                path = []
                while current_node in came_from:
                    path.append(current_node)
                    current_node = came_from[current_node]
                path.append(start)
                path.reverse() # Reverse it so it goes start -> goal
                return path, g_score[goal]
            
            # Explore neighboring intersections
            for neighbor in self.city.graph.neighbors(current_node):
                weight = self.city.get_weight(current_node, neighbor)
                tentative_g = g_score[current_node] + weight
                
                # If this is the fastest way we've found to this neighbor so far, save it
                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g
                    
                    # f(n) = g(n) + h(n)
                    f_score = tentative_g + self.heuristic(neighbor, goal)
                    counter += 1
                    heapq.heappush(frontier, (f_score, counter, neighbor))
                    
        return [], float('inf') # Return empty if no path is possible

# --- Execution Block ---
if __name__ == "__main__":
    city = CityGraph(5, 5)
    router = Pathfinder(city)
    
    ambulance_location = (0, 0)
    victim_location = (4, 4)
    
    print(f"Calculating route from {ambulance_location} to {victim_location}...")
    optimal_path, total_time = router.a_star(ambulance_location, victim_location)
    
    print(f"Optimal Path: {optimal_path}")
    print(f"Total Travel Time: {total_time:.2f} minutes")
    
    city.visualize(path=optimal_path)