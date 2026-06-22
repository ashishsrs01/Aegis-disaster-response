from src.perception.hazard_tracker import HazardTracker


def test_probability_range():
    tracker = HazardTracker()

    prob = tracker.infer_flood_probability(
        drone_observation="Yes",
        is_raining="Yes"
    )

    assert 0 <= prob <= 1


def test_sensor_positive_rainy_day():
    tracker = HazardTracker()

    prob = tracker.infer_flood_probability(
        drone_observation="Yes",
        is_raining="Yes"
    )

    assert prob > 0.5