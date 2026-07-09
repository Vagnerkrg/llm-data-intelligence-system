from typing import Dict

from src.agents.agent_registry import AgentRegistry
from src.agents.router.agent_router import AgentRouter
from src.agents.tools.bootstrap import register_default_tools
from src.agents.tools.registry import ToolRegistry
from src.agents.execution.tool_executor import ToolExecutor


class AgentController:
    """
    Central controller responsible for coordinating
    routing and execution of AI tools.

    The controller coordinates:

    - AgentRegistry for agent components;
    - ToolRegistry for available tools;
    - AgentRouter for tool selection;
    - ToolExecutor for execution lifecycle.
    """


    def __init__(
        self,
        registry=None,
        tool_registry=None,
        router=None,
        execution_executor=None
    ):

        self.registry = (
            registry
            if registry
            else AgentRegistry()
        )


        self.tool_registry = (
            tool_registry
            if tool_registry
            else ToolRegistry()
        )


        register_default_tools(
            self.tool_registry
        )


        self.router = (
            router
            if router
            else AgentRouter(
                self.tool_registry
            )
        )


        self.execution_executor = (
            execution_executor
            if execution_executor
            else ToolExecutor()
        )



    def run(
        self,
        question: str
    ) -> Dict:
        """
        Execute a user request through
        the routing and execution layers.
        """


        routing_result = self.router.route(
            question
        )


        if not routing_result.tool:

            return {

                "status": "error",

                "message": (
                    "No suitable tool found."
                ),

                "reason": routing_result.reason

            }



        tool = self.tool_registry.get_tool(
            routing_result.tool
        )


        if not tool:

            return {

                "status": "error",

                "message": (
                    "Tool not available."
                )

            }



        execution_result = (
            self.execution_executor.execute(
                tool,
                question
            )
        )


        return {

            "status": (
                "success"
                if execution_result.success
                else "error"
            ),

            "tool": execution_result.tool,

            "confidence": (
                routing_result.confidence
            ),

            "reason": (
                routing_result.reason
            ),

            "result": execution_result.data

        }