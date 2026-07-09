from src.agents.agent_registry import AgentRegistry


def test_register_component():

    registry = AgentRegistry()

    component = object()

    registry.register(
        "test_component",
        component
    )

    result = registry.get(
        "test_component"
    )

    assert result == component



def test_list_components():

    registry = AgentRegistry()

    registry.register(
        "analytics",
        object()
    )


    components = registry.list_components()


    assert "analytics" in components