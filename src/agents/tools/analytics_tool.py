from typing import Dict

from src.agents.data_analysis_agent import DataAnalysisAgent
from src.agents.tools.base_tool import BaseTool
from src.agents.tools.tool_metadata import ToolMetadata


class AnalyticsTool(BaseTool):
    """
    Tool responsible for exposing analytical capabilities
    to the agent layer.

    This adapter hides internal analytical implementation
    details from higher-level agents.

    The tool returns raw analytical data.
    Result normalization is handled by ToolExecutor.
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



    @property
    def metadata(self) -> ToolMetadata:
        """
        Return tool metadata information.
        """

        return ToolMetadata(

            name=self.name,

            description=self.description,

            capabilities=[

                "aggregation",

                "statistics",

                "dataset analysis"

            ]

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

        Returns raw analytical data.

        ToolResult creation is responsibility
        of ToolExecutor.
        """


        return self.agent.run(
            question
        )