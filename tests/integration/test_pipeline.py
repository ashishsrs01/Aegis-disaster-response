import pytest
from src.core.environment import CityGraph
from src.navigation.pathfinder import Pathfinder
from src.optimization.dispatcher import FleetDispatcher

def test_end_to_end_routing():
    """
    Test the full pipeline:
    1. Create environment
    2. Add hazard
    3. Calculate path
    4. Dispatch
    """
    # 1. Environment
    city = CityGraph(width=3, height=3)
    router = Pathfinder(city)
    dispatcher = FleetDispatcher()
    
    # 2. Block the direct path from (0,0) to (0,1)
    city.update_hazard_level((0, 0), (0, 1), probability=0.9) # Impassable
    
    # 3. Pathfinding
    start = (0, 0)
    goal = (0, 2)
    path, time = router.a_star(start, goal)
    
    # Since (0,0)->(0,1) is blocked, it must go around, so (0,1) shouldn't be in the path
    assert (0, 1) not in path
    
    # 4. Dispatch with mock data
    cost_matrix = [[time]] # 1 ambulance, 1 victim
    assignments = dispatcher.optimize_assignments(cost_matrix)
    
    assert assignments == [(0, 0)]
