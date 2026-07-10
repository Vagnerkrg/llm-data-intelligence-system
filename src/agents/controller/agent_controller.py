from typing import Dict

from src.agents.agent_registry import AgentRegistry
from src.agents.router.agent_router import AgentRouter
from src.agents.tools.bootstrap import register_default_tools
from src.agents.tools.registry import ToolRegistry
from src.agents.orchestration.tool_orchestrator import ToolOrchestrator
from src.agents.execution.tool_executor import ToolExecutor

from src.agents.planning.execution_planner import ExecutionPlanner
from src.agents.planning.execution_plan import ExecutionPlan



class AgentController:
    """
    Central controller responsible for coordinating
    routing, planning and execution of AI tools.

    The controller coordinates:

    - AgentRegistry;
    - ToolRegistry;
    - AgentRouter;
    - ExecutionPlanner;
    - ToolOrchestrator;
    - ToolExecutor;
    - AgentRuntime.
    """



    def __init__(
        self,
        registry=None,
        tool_registry=None,
        router=None,
        execution_executor=None,
        orchestrator=None,
        planner=None,
        runtime=None
    ):

        self.runtime = runtime


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


        self.orchestrator = (
            orchestrator
            if orchestrator
            else ToolOrchestrator(
                self.tool_registry,
                self.execution_executor
            )
        )


        self.planner = (
            planner
            if planner
            else ExecutionPlanner()
        )



    def create_plan(
        self,
        question: str
    ) -> ExecutionPlan:
        """
        Create an execution plan
        for a user request.
        """

        return self.planner.create_plan(
            question
        )



    def handle_request(
        self,
        question: str
    ):
        """
        Handle a user request through
        the AgentRuntime when available.

        The runtime becomes the preferred
        execution lifecycle in V1.10.
        """


        if self.runtime:

            return self.runtime.execute(
                question
            )


        return self.run(
            question
        )



    def run(
        self,
        question: str
    ) -> Dict:
        """
        Execute a user request through
        routing and orchestration layers.
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



        tools = [
            routing_result.tool
        ]



        orchestration_result = (
            self.orchestrator.execute(
                tools,
                question
            )
        )



        results = (
            orchestration_result.get(
                "results",
                []
            )
        )



        if not results:

            return {

                "status": "error",

                "message": (
                    "No execution result."
                )

            }



        return {

            "status": (
                "success"
                if all(
                    result.get("success")
                    for result in results
                )
                else "error"
            ),


            "tool": (
                tools[0]
                if len(tools) == 1
                else tools
            ),


            "tools_executed": (
                orchestration_result.get(
                    "tools_executed",
                    []
                )
            ),


            "confidence": (
                routing_result.confidence
            ),


            "reason": (
                routing_result.reason
            ),


            # Compatibilidade V1.9
            # mantém resposta simples
            # para consumidor único
            "result": (
                results[0]["data"]
                if len(results) == 1
                and "data" in results[0]
                else results
            ),


            # Novo contrato V1.10
            "results": results

        }