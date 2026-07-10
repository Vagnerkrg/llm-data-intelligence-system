from src.agents.planning.planner_strategy import PlannerStrategy


def test_planner_strategy_detects_analytics_request():

    strategy = PlannerStrategy()


    result = strategy.analyze(
        "Quantos produtos existem no dataset?"
    )


    assert result is not None

    assert result["type"] == "analytics"



def test_planner_strategy_detects_document_request():

    strategy = PlannerStrategy()


    result = strategy.analyze(
        "Explique o conteúdo deste documento"
    )


    assert result is not None

    assert result["type"] == "document"



def test_planner_strategy_returns_unknown_for_generic_request():

    strategy = PlannerStrategy()


    result = strategy.analyze(
        "Olá"
    )


    assert result is not None

    assert result["type"] == "unknown"