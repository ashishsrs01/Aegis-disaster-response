from src.optimization.dispatcher import FleetDispatcher


def test_hungarian_assignment():
    dispatcher = FleetDispatcher()

    matrix = [
        [4, 1, 3],
        [2, 0, 5],
        [3, 2, 2]
    ]

    assignments = dispatcher.optimize_assignments(matrix)

    assert len(assignments) == 3