import pytest
from src.optimization.dispatcher import FleetDispatcher

def test_dispatcher_assignments():
    """Test that the Hungarian algorithm correctly assigns ambulances to victims."""
    dispatcher = FleetDispatcher()
    
    # Cost matrix where:
    # Amb 0 is closest to Vic 1 (10 mins)
    # Amb 1 is closest to Vic 2 (12 mins)
    # Amb 2 is closest to Vic 0 (15 mins)
    cost_matrix = [
        [30.0, 10.0, 25.0],  # Amb 0
        [25.0, 35.0, 12.0],  # Amb 1
        [15.0, 20.0, 40.0]   # Amb 2
    ]
    
    assignments = dispatcher.optimize_assignments(cost_matrix)
    
    # Expected assignments to minimize total time:
    # (0, 1) -> 10.0
    # (1, 2) -> 12.0
    # (2, 0) -> 15.0
    
    assert (0, 1) in assignments
    assert (1, 2) in assignments
    assert (2, 0) in assignments
    assert len(assignments) == 3
