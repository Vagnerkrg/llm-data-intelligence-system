from src.cognitive.learning.patterns.pattern_detector import PatternDetector


def test_pattern_detector_creates_pattern():

    detector = PatternDetector()

    pattern = detector.detect(
        pattern_id="error-pattern",
        description="Falha recorrente",
        metadata={"source": "feedback"}
    )

    assert pattern.pattern_id == "error-pattern"
    assert pattern.frequency == 1
    assert detector.count() == 1



def test_pattern_detector_updates_existing_pattern():

    detector = PatternDetector()

    detector.detect(
        pattern_id="error-pattern",
        description="Falha recorrente"
    )

    pattern = detector.detect(
        pattern_id="error-pattern",
        description="Falha recorrente"
    )

    assert pattern.frequency == 2
    assert pattern.confidence > 0.5



def test_pattern_detector_returns_patterns():

    detector = PatternDetector()

    detector.detect(
        pattern_id="pattern-001",
        description="Teste"
    )

    patterns = detector.get_patterns()

    assert len(patterns) == 1
    assert patterns[0].pattern_id == "pattern-001"