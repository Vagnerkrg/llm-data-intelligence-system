from src.agents.router.agent_router import AgentRouter



def test_router_selects_analytics_tool():

    router = AgentRouter()


    result = router.route(
        "Quantos produtos existem?"
    )


    assert result.tool == "analytics"

    assert result.confidence > 0

    assert (
        "Analytical"
        in result.reason
    )



def test_router_selects_analytics_for_customer_query():

    router = AgentRouter()


    result = router.route(
        "Quantos clientes temos?"
    )


    assert result.tool == "analytics"



def test_router_returns_no_tool_for_unknown_query():

    router = AgentRouter()


    result = router.route(
        "Explique uma teoria qualquer"
    )


    assert result.tool is None

    assert result.confidence == 0.0