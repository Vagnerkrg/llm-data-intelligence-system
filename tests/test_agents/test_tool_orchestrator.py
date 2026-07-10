from src.agents.orchestration.tool_orchestrator import (
    ToolOrchestrator
)

from src.agents.tools.registry import ToolRegistry
from src.agents.tools.base_tool import BaseTool
from src.agents.tools.tool_metadata import ToolMetadata


class MockTool(BaseTool):

    name = "mock_tool"

    description = "Mock tool for testing"


    @property
    def metadata(self):

        return ToolMetadata(
            name=self.name,
            description=self.description
        )


    def execute(self, question):

        return {
            "answer": "mock result"
        }



def test_tool_orchestrator_executes_tool():

    registry = ToolRegistry()

    registry.register_tool(
        MockTool()
    )


    orchestrator = ToolOrchestrator(
        tool_registry=registry
    )


    result = orchestrator.execute(
        ["mock_tool"],
        "test question"
    )


    assert result["status"] == "success"

    assert result["tools_executed"] == 1

    assert (
        result["results"][0]["tool"]
        == "mock_tool"
    )



def test_tool_orchestrator_handles_missing_tool():

    registry = ToolRegistry()


    orchestrator = ToolOrchestrator(
        tool_registry=registry
    )


    result = orchestrator.execute(
        ["unknown_tool"],
        "test"
    )


    assert result["status"] == "success"

    assert (
        result["results"][0]["success"]
        is False
    )