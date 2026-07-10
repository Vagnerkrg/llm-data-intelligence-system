from typing import Any, Dict, List

from src.agents.tools.tool_result import ToolResult
from src.agents.execution.tool_executor import ToolExecutor


class ToolPipeline:
    """
    Coordinates execution of multiple tools in sequence.

    The pipeline allows agents to execute multiple specialized
    capabilities while preserving standardized ToolResult contracts.
    """

    def __init__(
        self,
        tool_executor: ToolExecutor,
        tools: List[str],
    ):
        self.tool_executor = tool_executor
        self.tools = tools

    def execute(
        self,
        request: Dict[str, Any],
    ) -> ToolResult:
        """
        Execute registered tools sequentially.

        Each tool receives the accumulated execution context.
        """

        results = []

        context = request.copy()

        for tool_name in self.tools:
            result = self.tool_executor.execute(
                tool_name,
                context,
            )

            results.append(result)

            if not result.success:
                return ToolResult(
                    tool="ToolPipeline",
                    success=False,
                    data={
                        "failed_tool": tool_name,
                        "results": results,
                    },
                    metadata={
                        "pipeline": self.tools,
                    },
                )

            context[tool_name] = result.data

        return ToolResult(
            tool="ToolPipeline",
            success=True,
            data={
                "results": results,
                "context": context,
            },
            metadata={
                "pipeline": self.tools,
                "steps": len(self.tools),
            },
        )