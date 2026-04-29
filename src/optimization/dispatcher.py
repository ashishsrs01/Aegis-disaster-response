import numpy as np
from scipy.optimize import linear_sum_assignment
from typing import List, Tuple

class FleetDispatcher:
    """
    Multi-agent optimization module.
    Assigns N ambulances to M victims minimizing total fleet travel time.
    """
    def __init__(self):
        pass

    def optimize_assignments(self, cost_matrix: List[List[float]]) -> List[Tuple[int, int]]:
        """
        Uses the Hungarian Algorithm (linear sum assignment) to find the 
        globally optimal dispatch strategy.
        
        cost_matrix[i][j] = time for Ambulance i to reach Victim j.
        """
        # Convert Python list to a high-performance NumPy array
        matrix = np.array(cost_matrix)
        
        # The algorithm returns the optimal row indices (ambulances) 
        # and column indices (victims)
        row_ind, col_ind = linear_sum_assignment(matrix)
        
        # Pair them up into a list of tuples: (Ambulance_Index, Victim_Index)
        assignments = list(zip(row_ind, col_ind))
        
        return assignments

# --- Execution Block ---
if __name__ == "__main__":
    dispatcher = FleetDispatcher()
    
    # Let's pretend we have 3 Ambulances and 3 Victims.
    # We ran A* Search in the background and got these travel times (in minutes):
    
    # Columns: Victim 0, Victim 1, Victim 2
    mock_cost_matrix = [
        [15.0, 10.0, 30.0],  # Ambulance 0's travel times
        [25.0, 35.0, 12.0],  # Ambulance 1's travel times
        [20.0, 15.0, 40.0]   # Ambulance 2's travel times
    ]
    
    print("Cost Matrix (Travel Times):")
    for i, row in enumerate(mock_cost_matrix):
        print(f"Ambulance {i}: {row}")
        
    print("\nCalculating Global Optimum...")
    optimal_pairs = dispatcher.optimize_assignments(mock_cost_matrix)
    
    total_fleet_time = 0
    for amb_idx, vic_idx in optimal_pairs:
        time = mock_cost_matrix[amb_idx][vic_idx]
        total_fleet_time += time
        print(f"DISPATCH: Ambulance {amb_idx} -> Victim {vic_idx} (Time: {time} mins)")
        
    print(f"\nTotal Fleet Travel Time: {total_fleet_time} mins")