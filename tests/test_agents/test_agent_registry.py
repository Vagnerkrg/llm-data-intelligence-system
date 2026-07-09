from src.agents.agent_registry import AgentRegistry
from src.agents.tools.analytics_tool import AnalyticsTool



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



def test_registry_returns_tool_metadata():

    registry = AgentRegistry()


    tool = AnalyticsTool()


    registry.register_tool(
        tool
    )


    metadata = registry.list_tool_metadata()


    assert len(metadata) == 1


    assert metadata[0].name == "analytics"


    assert (
        "statistics"
        in metadata[0].capabilities
    )