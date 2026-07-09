from typing import Dict

from src.agents.tools.base_tool import BaseTool
from src.agents.tools.tool_metadata import ToolMetadata
from src.rag.query_engine import RAGQueryEngine


class RAGTool(BaseTool):
    """
    Tool responsible for exposing
    Retrieval Augmented Generation capabilities
    to the agent layer.

    This adapter hides RAG implementation details
    from agents.

    Result normalization is handled by ToolExecutor.
    """

    def __init__(
        self,
        query_engine=None
    ):
        self.query_engine = (
            query_engine
            if query_engine
            else RAGQueryEngine()
        )


    @property
    def name(self) -> str:
        """
        Tool identifier.
        """

        return "rag"



    @property
    def description(self) -> str:
        """
        Human-readable tool description.
        """

        return (
            "Retrieves contextual information "
            "using semantic search and RAG generation."
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

                "semantic search",

                "knowledge retrieval",

                "context retrieval",

                "question answering"

            ]

        )



    def execute(
        self,
        question: str
    ) -> Dict:
        """
        Execute RAG query.

        Returns raw RAG response.

        ToolResult creation is responsibility
        of ToolExecutor.
        """

        return self.query_engine.query(
            question
        )