from src.core.environment import CityGraph
from src.navigation.pathfinder import Pathfinder
from src.optimization.dispatcher import FleetDispatcher
from src.core.victim import Victim

def main():
    print("Initializing Aegis Disaster Response System...")
    # Make a slightly larger city for the fleet
    city = CityGraph(width=8, height=8)
    router = Pathfinder(city)
    dispatcher = FleetDispatcher()
    
    # 1. Define the Fleet (Ambulance Starting Locations)
    ambulances = [(0, 0), (7, 0), (0, 7)]
    
    # 2. Define the Victims scattered across the city
    victims = [
        Victim(id=0, location=(4, 4), vitals={'breathing': True, 'conscious': False}),
        Victim(id=1, location=(6, 2), vitals={'breathing': True, 'conscious': True}),
        Victim(id=2, location=(2, 6), vitals={'breathing': True, 'conscious': False})
    ]
    
    # 3. Build the Dynamic Cost Matrix using A* Search
    print("Calculating environment geometry and A* travel times...")
    cost_matrix = []
    
    for i, amb_loc in enumerate(ambulances):
        amb_costs = []
        for j, vic in enumerate(victims):
            # Run A* to find the actual travel time accounting for road weights
            path, travel_time = router.a_star(amb_loc, vic.location)
            amb_costs.append(travel_time)
            
        cost_matrix.append(amb_costs)
        print(f"Ambulance {i} evaluated all targets.")
        
    # 4. Run Multi-Agent Optimization
    print("\nExecuting Operations Research (Hungarian Algorithm)...")
    optimal_assignments = dispatcher.optimize_assignments(cost_matrix)
    
    # 5. Output the final global strategy
    print("\n=== OPTIMAL FLEET DISPATCH STRATEGY ===")
    total_time = 0
    for amb_idx, vic_idx in optimal_assignments:
        amb_loc = ambulances[amb_idx]
        vic_loc = victims[vic_idx].location
        time = cost_matrix[amb_idx][vic_idx]
        total_time += time
        print(f"DISPATCH: Ambulance {amb_idx} {amb_loc} -> Victim {vic_idx} {vic_loc} (ETA: {time:.2f} mins)")
        
    print(f"\nTotal Fleet Action Time: {total_time:.2f} mins")

if __name__ == "__main__":
    main()