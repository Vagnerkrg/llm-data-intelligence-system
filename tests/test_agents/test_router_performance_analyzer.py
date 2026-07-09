from src.agents.evaluation.routing_history import RoutingHistory
from src.agents.evaluation.routing_evaluator import RoutingEvaluation
from src.agents.evaluation.router_performance_analyzer import (
    RouterPerformanceAnalyzer
)

from datetime import datetime



def create_evaluation(
    tool,
    confidence,
    success
):

    return RoutingEvaluation(

        question="test question",

        selected_tool=tool,

        confidence=confidence,

        success=success,

        timestamp=datetime.now()

    )



def test_total_decisions():

    history = RoutingHistory()


    history.add(
        create_evaluation(
            "analytics",
            0.9,
            True
        )
    )


    history.add(
        create_evaluation(
            "analytics",
            0.7,
            False
        )
    )


    analyzer = RouterPerformanceAnalyzer(
        history
    )


    assert analyzer.total_decisions() == 2



def test_success_rate_by_tool():

    history = RoutingHistory()


    history.add(
        create_evaluation(
            "analytics",
            0.9,
            True
        )
    )


    history.add(
        create_evaluation(
            "analytics",
            0.8,
            False
        )
    )


    analyzer = RouterPerformanceAnalyzer(
        history
    )


    result = analyzer.success_rate_by_tool()


    assert result["analytics"] == 0.5



def test_average_confidence_by_tool():

    history = RoutingHistory()


    history.add(
        create_evaluation(
            "analytics",
            0.8,
            True
        )
    )


    history.add(
        create_evaluation(
            "analytics",
            0.6,
            True
        )
    )


    analyzer = RouterPerformanceAnalyzer(
        history
    )


    result = analyzer.average_confidence_by_tool()


    assert result["analytics"] == 0.7



def test_best_tool():

    history = RoutingHistory()


    history.add(
        create_evaluation(
            "analytics",
            0.9,
            True
        )
    )


    history.add(
        create_evaluation(
            "analytics",
            0.8,
            True
        )
    )


    history.add(
        create_evaluation(
            "search",
            0.7,
            False
        )
    )


    analyzer = RouterPerformanceAnalyzer(
        history
    )


    assert (
        analyzer.best_tool()
        ==
        "analytics"
    )