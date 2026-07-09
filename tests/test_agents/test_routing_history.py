from datetime import datetime

from src.agents.evaluation.routing_evaluator import RoutingEvaluation
from src.agents.evaluation.routing_history import RoutingHistory



def test_routing_history_add_record():

    history = RoutingHistory()


    evaluation = RoutingEvaluation(

        question="Quantos clientes existem?",

        selected_tool="analytics",

        confidence=0.9,

        success=True,

        timestamp=datetime.now()

    )


    history.add(
        evaluation
    )


    assert history.count() == 1



def test_routing_history_returns_records():

    history = RoutingHistory()


    evaluation = RoutingEvaluation(

        question="Analise dados",

        selected_tool="analytics",

        confidence=0.8,

        success=True,

        timestamp=datetime.now()

    )


    history.add(
        evaluation
    )


    records = history.all()


    assert len(records) == 1

    assert (
        records[0].selected_tool
        ==
        "analytics"
    )