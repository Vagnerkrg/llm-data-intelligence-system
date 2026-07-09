from typing import List

from src.agents.tools.registry import ToolRegistry
from src.agents.tools.base_tool import BaseTool
from src.agents.tools.analytics_tool import AnalyticsTool



def get_default_tools() -> List[BaseTool]:
    """
    Return the default tools available
    in the agent ecosystem.
    """

    return [

        AnalyticsTool()

    ]



def register_default_tools(
    registry: ToolRegistry
):
    """
    Register default available tools
    into the tool registry.
    """


    for tool in get_default_tools():

        registry.register_tool(
            tool
        )