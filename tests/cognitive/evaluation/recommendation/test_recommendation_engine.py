from src.cognitive.evaluation.decision.evaluation_decision import (
    EvaluationDecision,
)

from src.cognitive.evaluation.recommendation.recommendation_engine import (
    RecommendationEngine,
)

from src.cognitive.evaluation.recommendation.evaluation_recommendation import (
    EvaluationRecommendation,
)



def test_recommendation_engine_creates_improvement_strategy():

    decision = EvaluationDecision(
        action="adapt",
        priority="high",
        target="reasoning",
    )


    engine = RecommendationEngine()


    recommendation = engine.recommend(
        decision
    )


    assert isinstance(
        recommendation,
        EvaluationRecommendation
    )


    assert recommendation.strategy == "improve_reasoning"

    assert recommendation.confidence >= 0.8



def test_recommendation_engine_keeps_good_behavior():

    decision = EvaluationDecision(
        action="maintain",
        priority="low",
        target="general",
    )


    engine = RecommendationEngine()


    recommendation = engine.recommend(
        decision
    )


    assert recommendation.strategy == "continue_current_behavior"

    assert recommendation.confidence == 1.0