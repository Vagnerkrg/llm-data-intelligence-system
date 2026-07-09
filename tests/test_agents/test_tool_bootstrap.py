from src.agents.agent_registry import AgentRegistry
from src.agents.tools.bootstrap import register_default_tools



def test_register_default_tools():

    registry = AgentRegistry()


    register_default_tools(
        registry
    )


    tools = registry.list_tools()


    assert "analytics" in tools



def test_default_tools_are_registered_as_metadata():

    registry = AgentRegistry()


    register_default_tools(
        registry
    )


    metadata = registry.list_tool_metadata()


    assert len(metadata) == 1


    assert metadata[0].name == "analytics"