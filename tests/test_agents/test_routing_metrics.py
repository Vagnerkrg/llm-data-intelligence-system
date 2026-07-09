from datetime import datetime

from src.agents.evaluation.routing_history import RoutingHistory
from src.agents.evaluation.routing_metrics import RoutingMetrics
from src.agents.evaluation.routing_evaluator import RoutingEvaluation



def create_evaluation(
    tool,
    confidence,
    success
):

    return RoutingEvaluation(

        question="Test question",

        selected_tool=tool,

        confidence=confidence,

        success=success,

        timestamp=datetime.now()

    )



def test_total_routes():

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


    metrics = RoutingMetrics(
        history
    )


    assert metrics.total_routes() == 2



def test_average_confidence():

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


    metrics = RoutingMetrics(
        history
    )


    assert metrics.average_confidence() == 0.7



def test_success_rate():

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
            None,
            0.0,
            False
        )
    )


    metrics = RoutingMetrics(
        history
    )


    assert metrics.success_rate() == 0.5



def test_tool_usage():

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
            True
        )
    )


    metrics = RoutingMetrics(
        history
    )


    usage = metrics.tool_usage()


    assert usage["analytics"] == 2

    assert usage["search"] == 1



def test_empty_history_metrics():

    history = RoutingHistory()


    metrics = RoutingMetrics(
        history
    )


    assert metrics.total_routes() == 0

    assert metrics.average_confidence() == 0.0

    assert metrics.success_rate() == 0.0

    assert metrics.tool_usage() == {}