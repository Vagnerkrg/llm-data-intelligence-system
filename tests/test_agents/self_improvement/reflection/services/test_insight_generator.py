from src.agents.self_improvement.reflection.services import (
    InsightGenerator,
)


def test_should_initialize_insight_generator():

    generator = InsightGenerator()

    assert generator is not None


def test_should_generate_insight():

    generator = InsightGenerator()

    hypothesis = {
        "title": "Execution Optimization",
        "description": "Execution strategy improved",
        "confidence": 0.9,
    }

    insight = generator.generate(hypothesis)

    assert insight is not None


def test_should_generate_high_confidence_insight():

    generator = InsightGenerator()

    hypothesis = {
        "title": "Performance Improvement",
        "description": "Latency decreased",
        "confidence": 0.95,
    }

    insight = generator.generate(hypothesis)

    assert insight.confidence == 0.95
