from src.agents.decision.confidence_analyzer import ConfidenceAnalyzer
from src.agents.decision.alternative_evaluation import AlternativeEvaluation


def test_confidence_analyzer_calculates_confidence():

    evaluations = [
        AlternativeEvaluation(
            alternative_id="strategy_a",
            score=0.6,
            confidence=0.6,
            risk_level="medium",
            evaluation_reason="acceptable"
        ),
        AlternativeEvaluation(
            alternative_id="strategy_b",
            score=0.9,
            confidence=0.9,
            risk_level="low",
            evaluation_reason="best option"
        )
    ]

    analyzer = ConfidenceAnalyzer()

    confidence = analyzer.calculate(
        evaluations
    )

    assert confidence == 0.9