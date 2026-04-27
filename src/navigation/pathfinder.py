import heapq
from typing import List, Tuple, Dict
from src.core.environment import CityGraph

class Pathfinder:
    """
    Handles routing for agents through the city graph.
    """
    def __init__(self, city: CityGraph):
        self.city = city

    def manhattan_distance(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """The heuristic function h(n). Calculates grid block distance."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], float]:
        """
        A* Search Algorithm. 
        Finds the fastest path considering road weights (traffic/hazards).
        """
        # Priority Queue: Always pops the node with the lowest f_score
        frontier = []
        heapq.heappush(frontier, (0, start))
        
        # Keep track of where we came from to reconstruct the final route
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        
        # g_score: Actual travel time from start to a specific node
        g_score = {node: float('inf') for node in self.city.graph.nodes()}
        g_score[start] = 0
        
        while frontier:
            # Get the node with the lowest estimated total cost
            current_f, current_node = heapq.heappop(frontier)
            
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
                # Calculate time to move to this neighbor
                weight = self.city.get_weight(current_node, neighbor)
                tentative_g = g_score[current_node] + weight
                
                # If this is the fastest way we've found to this neighbor so far, save it
                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g
                    
                    # f(n) = g(n) + h(n)
                    f_score = tentative_g + self.manhattan_distance(neighbor, goal)
                    heapq.heappush(frontier, (f_score, neighbor))
                    
        return [], float('inf') # Return empty if no path is possible

# --- Execution Block ---
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
    
    # Render the result
    city.visualize(path=optimal_path)