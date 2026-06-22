import pytest
from src.core.environment import CityGraph

def test_city_graph_initialization():
    """Test that the city graph is created with correct dimensions."""
    city = CityGraph(width=3, height=3)
    
    # 3x3 grid should have 9 intersections (nodes)
    assert city.graph.number_of_nodes() == 9
    
    # 3x3 grid has 12 roads (edges)
    assert city.graph.number_of_edges() == 12

def test_get_weight_existing_road():
    """Test that we can retrieve a travel time for an existing road."""
    city = CityGraph(width=3, height=3)
    
    # Nodes (0,0) and (0,1) are adjacent in a grid graph
    weight = city.get_weight((0, 0), (0, 1))
    
    # Weight should be between 1.0 and 3.0 as initialized
    assert 1.0 <= weight <= 3.0

def test_get_weight_non_existent_road():
    """Test that a non-existent road returns infinite cost."""
    city = CityGraph(width=3, height=3)
    
    # Nodes (0,0) and (2,2) are NOT directly connected
    weight = city.get_weight((0, 0), (2, 2))
    
    # Weight should be infinity
    assert weight == float('inf')

def test_update_hazard_level():
    """Test that updating hazard probability changes the road weight."""
    city = CityGraph(width=3, height=3)
    
    # Apply a high probability hazard
    city.update_hazard_level((0, 0), (0, 1), probability=0.9)
    
    # The weight should now be 999.0 (impassable)
    assert city.get_weight((0, 0), (0, 1)) == 999.0