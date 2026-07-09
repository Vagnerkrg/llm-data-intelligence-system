from src.agents.router.agent_router import AgentRouter



def test_router_selects_analytics_tool():

    router = AgentRouter()


    tool = router.route(
        "Quantos produtos existem?"
    )


    assert tool == "analytics"



def test_router_selects_analytics_for_customer_query():

    router = AgentRouter()


    tool = router.route(
        "Quantos clientes temos?"
    )


    assert tool == "analytics"



def test_router_returns_none_for_unknown_query():

    router = AgentRouter()


    tool = router.route(
        "Explique uma teoria qualquer"
    )


    assert tool is None