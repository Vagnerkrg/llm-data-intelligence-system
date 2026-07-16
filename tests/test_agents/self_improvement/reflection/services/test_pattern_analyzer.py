from src.agents.self_improvement.reflection.services import (
    PatternAnalyzer,
)


def test_should_initialize_pattern_analyzer():

    analyzer = PatternAnalyzer()

    assert analyzer is not None


def test_should_analyze_empty_data():

    analyzer = PatternAnalyzer()

    result = analyzer.analyze([])

    assert result == []


def test_should_detect_performance_pattern():

    analyzer = PatternAnalyzer()

    data = [
        {
            "metric": "execution_time",
            "value": 10,
        },
        {
            "metric": "execution_time",
            "value": 8,
        },
        {
            "metric": "execution_time",
            "value": 6,
        },
    ]

    patterns = analyzer.analyze(data)

    assert len(patterns) > 0
