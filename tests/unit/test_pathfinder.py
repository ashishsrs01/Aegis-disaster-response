from src.core.environment import CityGraph
from src.navigation.pathfinder import Pathfinder


def test_a_star_finds_path():
    city = CityGraph(5, 5)
    router = Pathfinder(city)

    path, cost = router.a_star((0, 0), (4, 4))

    assert path is not None
    assert len(path) > 0
    assert cost > 0


def test_path_starts_and_ends_correctly():
    city = CityGraph(5, 5)
    router = Pathfinder(city)

    path, cost = router.a_star((0, 0), (4, 4))

    assert path[0] == (0, 0)
    assert path[-1] == (4, 4)