from src.agents.tools.base_tool import BaseTool
from src.agents.tools.tool_result import ToolResult


class ToolExecutor:
    """
    Execution layer responsible for running tools
    and normalizing execution results.
    """


    def execute(
        self,
        tool: BaseTool,
        question: str
    ) -> ToolResult:
        """
        Execute a tool and return
        a standardized ToolResult.
        """


        try:

            result = tool.execute(
                question
            )


            return ToolResult(

                tool=tool.name,

                success=True,

                data=result,

                metadata={

                    "description": getattr(
                        tool,
                        "description",
                        ""
                    )

                }

            )


        except Exception as error:


            return ToolResult(

                tool=getattr(
                    tool,
                    "name",
                    "unknown"
                ),

                success=False,

                data={

                    "error": str(error)

                },

                metadata={

                    "description": getattr(
                        tool,
                        "description",
                        ""
                    )

                }

            )