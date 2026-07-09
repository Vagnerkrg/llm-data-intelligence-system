from typing import Dict

from src.agents.agent_registry import AgentRegistry
from src.agents.router.agent_router import AgentRouter
from src.agents.tools.analytics_tool import AnalyticsTool


class AgentController:
    """
    Central controller responsible for coordinating
    routing and execution of AI tools.
    """


    def __init__(
        self,
        registry=None,
        router=None
    ):

        self.registry = (
            registry
            if registry
            else AgentRegistry()
        )


        self.router = (
            router
            if router
            else AgentRouter()
        )


        self._register_default_tools()



    def _register_default_tools(self):
        """
        Register default system tools.
        """

        analytics_tool = AnalyticsTool()


        self.registry.register_tool(
            analytics_tool
        )



    def run(
        self,
        question: str
    ) -> Dict:
        """
        Execute a user request through
        the routing layer.
        """


        tool_name = self.router.route(
            question
        )


        if not tool_name:

            return {

                "status": "error",

                "message": (
                    "No suitable tool found."
                )

            }



        tool = self.registry.get_tool(
            tool_name
        )


        if not tool:

            return {

                "status": "error",

                "message": (
                    "Tool not available."
                )

            }



        result = tool.execute(
            question
        )


        return {

            "status": "success",

            "tool": tool.name,

            "result": result

        }