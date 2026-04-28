from src.core.environment import CityGraph
from src.navigation.pathfinder import Pathfinder
from src.perception.hazard_tracker import HazardTracker

def main():
    
    # 1. Setup
    city = CityGraph(width=7, height=7)
    tracker = HazardTracker()
    router = Pathfinder(city)
    
    start = (0, 0)
    goal = (6, 6)
    
    # 2. Initial Path (The "Optimistic" Route)
    print("--- Scenario 1: No Hazards ---")
    path1, time1 = router.a_star(start, goal)
    print(f"Original Time: {time1:.2f} mins")

    # 3. The Disaster Happens! 
    # A drone senses a flood at an intersection right in the middle of our path
    flood_node = path1[len(path1)//2] 
    neighbor = (flood_node[0] + 1, flood_node[1])
    
    print(f"\n--- Scenario 2: Hazard Detected at {flood_node} ---")
    
    # Drone says "I see a flood", and it's raining
    prob = tracker.infer_flood_probability(drone_observation='Yes', is_raining='Yes')
    
    # Update the city map with this "intelligence"
    city.update_hazard_level(flood_node, neighbor, prob)
    
    # 4. Re-calculate Path (The "Adaptive" Route)
    path2, time2 = router.a_star(start, goal)
    print(f"New Time: {time2:.2f} mins")
    
    if path1 == path2:
        print("ALERT: Agent did not change path. Weight might not be high enough.")
    else:
        print("SUCCESS: Agent found a safer detour!")

    # 5. Visualize the detour
    city.visualize(path=path2)

if __name__ == "__main__":
    main()