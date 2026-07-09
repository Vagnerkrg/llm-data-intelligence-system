from src.agents.tools.registry import ToolRegistry
from src.agents.tools.analytics_tool import AnalyticsTool
from src.agents.tools.base_tool import BaseTool
from src.agents.tools.tool_metadata import ToolMetadata



class DisabledTestTool(BaseTool):
    """
    Fake disabled tool used
    to test registry filtering.
    """


    @property
    def name(self):

        return "disabled_tool"



    @property
    def description(self):

        return "Disabled test tool."



    @property
    def metadata(self):

        return ToolMetadata(

            name=self.name,

            description=self.description,

            capabilities=[

                "testing"

            ],

            enabled=False

        )



    def execute(
        self,
        *args,
        **kwargs
    ):

        return {}



def test_register_tool():

    registry = ToolRegistry()

    tool = AnalyticsTool()


    registry.register_tool(
        tool
    )


    result = registry.get_tool(
        "analytics"
    )


    assert result == tool



def test_list_tools():

    registry = ToolRegistry()


    registry.register_tool(
        AnalyticsTool()
    )


    tools = registry.list_tools()


    assert "analytics" in tools



def test_registry_returns_tool_metadata():

    registry = ToolRegistry()


    registry.register_tool(
        AnalyticsTool()
    )


    metadata = registry.list_tool_metadata()


    assert len(metadata) == 1


    assert metadata[0].name == "analytics"


    assert (
        "statistics"
        in metadata[0].capabilities
    )



def test_find_tools_by_capability():

    registry = ToolRegistry()


    registry.register_tool(
        AnalyticsTool()
    )


    tools = registry.find_tools_by_capability(
        "statistics"
    )


    assert len(tools) == 1

    assert tools[0].name == "analytics"



def test_list_active_tools():

    registry = ToolRegistry()


    registry.register_tool(
        AnalyticsTool()
    )


    registry.register_tool(
        DisabledTestTool()
    )


    tools = registry.list_active_tools()


    assert len(tools) == 1

    assert tools[0].name == "analytics"



def test_ignore_disabled_tools():

    registry = ToolRegistry()


    registry.register_tool(
        DisabledTestTool()
    )


    tools = registry.find_active_tools_by_capability(
        "testing"
    )


    assert len(tools) == 0