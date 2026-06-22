from src.reasoning.triage import TriageEngine


def test_black_tag():
    engine = TriageEngine()

    result = engine.evaluate({
        "breathing": False
    })

    assert result == "BLACK"


def test_red_tag_unconscious():
    engine = TriageEngine()

    result = engine.evaluate({
        "breathing": True,
        "conscious": False
    })

    assert result == "RED"


def test_yellow_tag():
    engine = TriageEngine()

    result = engine.evaluate({
        "breathing": True,
        "conscious": True,
        "pulse": True
    })

    assert result == "YELLOW"