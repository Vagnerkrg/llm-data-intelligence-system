from src.agents.execution.tool_executor import ToolExecutor
from src.agents.tools.analytics_tool import AnalyticsTool



class BrokenTool:

    name = "broken"



    def execute(
        self,
        question: str
    ):

        raise Exception(
            "Execution failed"
        )



def test_tool_executor_success():

    executor = ToolExecutor()

    tool = AnalyticsTool()


    result = executor.execute(

        tool,

        "Quantos produtos existem?"

    )


    assert result.success is True

    assert result.tool == "analytics"

    assert (
        result.data["type"]
        ==
        "analysis"
    )



def test_tool_executor_failure():

    executor = ToolExecutor()


    result = executor.execute(

        BrokenTool(),

        "test"

    )


    assert result.success is False

    assert (
        result.data["error"]
        ==
        "Execution failed"
    )