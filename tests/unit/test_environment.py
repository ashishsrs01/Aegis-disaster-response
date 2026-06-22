from src.core.environment import CityGraph

def test_grid_node_count():
    city = CityGraph(5, 5)

    assert city.graph.number_of_nodes() == 25


def test_grid_has_edges():
    city = CityGraph(5, 5)

    assert city.graph.number_of_edges() > 0