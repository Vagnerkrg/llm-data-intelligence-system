from src.agents.controller.agent_controller import AgentController
from src.agents.execution.tool_executor import ToolExecutor


class FakeExecutor(ToolExecutor):
    def __init__(self):
        self.executed = False

    def execute(self, tool, question):

        self.executed = True

        return type(
            "FakeResult",
            (),
            {
                "success": True,
                "tool": tool.name,
                "data": {"type": "analysis"},
                "metadata": {},
            },
        )()


def test_agent_controller_uses_executor():

    executor = FakeExecutor()

    controller = AgentController(execution_executor=executor)

    response = controller.run("quantos produtos existem?")

    assert response["status"] == "success"

    assert response["tool"] == "analytics"

    assert executor.executed is True
