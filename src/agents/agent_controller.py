from typing import Dict

from src.agents.agent_registry import AgentRegistry
from src.agents.tools.analytics_tool import AnalyticsTool


class AgentController:
    """
    Central controller responsible for coordinating
    available AI tools and agents.
    """


    def __init__(
        self,
        registry=None
    ):

        self.registry = (
            registry
            if registry
            else AgentRegistry()
        )


        self._register_default_tools()



    def _register_default_tools(self):
        """
        Register default system tools.
        """

        analytics_tool = AnalyticsTool()

        self.registry.register(
            analytics_tool.name,
            analytics_tool
        )



    def run(
        self,
        question: str
    ) -> Dict:
        """
        Execute a user request using
        the appropriate registered tool.
        """

        tool = self._select_tool(
            question
        )


        if not tool:

            return {

                "status": "error",

                "message": (
                    "No suitable tool found."
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



    def _select_tool(
        self,
        question: str
    ):

        text = question.lower()


        analytical_keywords = [

            "quantos",

            "categoria",

            "colunas",

            "dados",

            "produtos",

            "clientes"

        ]


        if any(
            keyword in text
            for keyword in analytical_keywords
        ):

            return self.registry.get(
                "analytics"
            )


        return None