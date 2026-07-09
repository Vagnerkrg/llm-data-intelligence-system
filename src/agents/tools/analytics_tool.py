from typing import Dict

from src.agents.data_analysis_agent import DataAnalysisAgent
from src.agents.tools.base_tool import BaseTool


class AnalyticsTool(BaseTool):
    """
    Tool responsible for exposing analytical capabilities
    to the agent layer.

    This adapter hides internal analytical implementation
    details from higher-level agents.
    """


    @property
    def name(self) -> str:
        return "analytics"


    @property
    def description(self) -> str:
        return (
            "Executes structured data analysis "
            "using available datasets."
        )


    def __init__(
        self,
        analysis_agent=None
    ):

        self.agent = (
            analysis_agent
            if analysis_agent
            else DataAnalysisAgent()
        )


    def execute(
        self,
        question: str
    ) -> Dict:
        """
        Execute analytical requests.
        """

        return self.agent.run(
            question
        )