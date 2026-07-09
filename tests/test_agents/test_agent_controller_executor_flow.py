from src.agents.controller.agent_controller import AgentController
from src.agents.execution.tool_executor import ToolExecutor
from src.agents.tools.registry import ToolRegistry


class FakeExecutor:

    def __init__(self):

        self.called = False


    def execute(
        self,
        tool,
        question
    ):

        self.called = True

        return type(
            "Result",
            (),
            {
                "success": True,
                "tool": tool.name,
                "data": {
                    "executed_by": "executor"
                }
            }
        )()



def test_agent_controller_uses_tool_executor():

    executor = FakeExecutor()


    controller = AgentController(
        execution_executor=executor
    )


    response = controller.run(
        "Quantos produtos existem?"
    )


    assert executor.called is True

    assert response["status"] == "success"

    assert (
        response["result"]["executed_by"]
        ==
        "executor"
    )