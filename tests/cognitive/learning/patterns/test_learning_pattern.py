from src.cognitive.learning.patterns.learning_pattern import LearningPattern


def test_learning_pattern_creation():

    pattern = LearningPattern(
        pattern_id="pattern-001",
        description="Erro recorrente de execução",
        frequency=1,
        confidence=0.5,
        metadata={},
    )

    assert pattern.pattern_id == "pattern-001"
    assert pattern.frequency == 1
    assert pattern.confidence == 0.5


def test_learning_pattern_frequency_increment():

    pattern = LearningPattern(
        pattern_id="pattern-001",
        description="Teste",
        frequency=1,
        confidence=0.5,
        metadata={},
    )

    pattern.increase_frequency()

    assert pattern.frequency == 2


def test_learning_pattern_strength():

    pattern = LearningPattern(
        pattern_id="pattern-001",
        description="Teste",
        frequency=1,
        confidence=0.6,
        metadata={},
    )

    pattern.strengthen(0.2)

    assert pattern.confidence == 0.8
    assert pattern.is_reliable()
