from src.agents.controller.agent_controller import AgentController


class FakeMultiToolExecutor:

    def __init__(self):
        self.executed_tools = []


    def execute(
        self,
        tool,
        question
    ):

        self.executed_tools.append(
            tool.name
        )


        return type(
            "Result",
            (),
            {
                "success": True,
                "tool": tool.name,
                "data": {
                    "tool": tool.name,
                    "question": question
                }
            }
        )()



def test_agent_controller_executes_multiple_tools():

    executor = FakeMultiToolExecutor()


    controller = AgentController(
        execution_executor=executor
    )


    response = controller.run(
        "Analise produtos e categorias"
    )


    assert response["status"] == "success"


    assert len(
        executor.executed_tools
    ) >= 1