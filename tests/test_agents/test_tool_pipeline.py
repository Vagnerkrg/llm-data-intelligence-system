from src.agents.execution.tool_pipeline import ToolPipeline
from src.agents.tools.tool_result import ToolResult


class MockToolExecutor:

    def __init__(self):
        self.calls = []

    def execute(self, tool_name, data):

        self.calls.append(tool_name)

        return ToolResult(
            tool=tool_name,
            success=True,
            data={
                "tool": tool_name,
                "processed": True,
            },
            metadata={},
        )


def test_tool_pipeline_executes_multiple_tools():

    executor = MockToolExecutor()

    pipeline = ToolPipeline(
        tool_executor=executor,
        tools=[
            "rag_tool",
            "analytics_tool",
        ],
    )

    result = pipeline.execute(
        {
            "query": "analyze dataset",
        }
    )

    assert result.success is True

    assert executor.calls == [
        "rag_tool",
        "analytics_tool",
    ]


def test_tool_pipeline_returns_results():

    executor = MockToolExecutor()

    pipeline = ToolPipeline(
        tool_executor=executor,
        tools=[
            "rag_tool",
            "analytics_tool",
        ],
    )

    result = pipeline.execute(
        {
            "query": "test",
        }
    )

    assert "results" in result.data

    assert len(result.data["results"]) == 2


def test_tool_pipeline_preserves_context():

    executor = MockToolExecutor()

    pipeline = ToolPipeline(
        tool_executor=executor,
        tools=[
            "rag_tool",
        ],
    )

    result = pipeline.execute(
        {
            "input": "hello",
        }
    )

    assert result.success is True

    assert "context" in result.data