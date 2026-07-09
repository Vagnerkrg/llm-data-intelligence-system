from src.agents.agent_registry import AgentRegistry
from src.agents.tools.analytics_tool import AnalyticsTool



def register_default_tools(
    registry: AgentRegistry
):
    """
    Register default available tools
    into the agent registry.
    """


    analytics_tool = AnalyticsTool()


    registry.register_tool(
        analytics_tool
    )