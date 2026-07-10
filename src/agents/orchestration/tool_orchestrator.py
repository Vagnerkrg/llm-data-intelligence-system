from typing import Dict, List

from src.agents.execution.tool_executor import ToolExecutor
from src.agents.tools.registry import ToolRegistry


class ToolOrchestrator:
    """
    Coordinates execution of multiple tools.

    Responsible for:
    - receiving selected tools;
    - executing tools through ToolExecutor;
    - collecting execution results;
    - returning a consolidated response.
    """

    def __init__(
        self,
        tool_registry=None,
        executor=None
    ):

        self.tool_registry = (
            tool_registry
            if tool_registry
            else ToolRegistry()
        )

        self.executor = (
            executor
            if executor
            else ToolExecutor()
        )


    def execute(
        self,
        tools: List[str],
        question: str
    ) -> Dict:
        """
        Execute multiple tools sequentially.

        Parameters:
            tools:
                List of tool names.

            question:
                User request.

        Returns:
            Consolidated execution result.
        """

        results = []


        for tool_name in tools:

            tool = self.tool_registry.get_tool(
                tool_name
            )


            if not tool:

                results.append(
                    {
                        "tool": tool_name,
                        "success": False,
                        "error": "Tool not found"
                    }
                )

                continue



            execution_result = (
                self.executor.execute(
                    tool,
                    question
                )
            )



            results.append(
                {
                    "tool": execution_result.tool,

                    "success": (
                        execution_result.success
                    ),

                    "data": (
                        execution_result.data
                    ),

                    "metadata": (
                        getattr(
                            execution_result,
                            "metadata",
                            {}
                        )
                    )
                }
            )



        return {
            "status": "success",
            "tools_executed": len(results),
            "results": results
        }