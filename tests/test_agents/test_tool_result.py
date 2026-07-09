from src.agents.tools.tool_result import ToolResult



def test_tool_result_creation():

    result = ToolResult(

        tool="analytics",

        success=True,

        data={

            "records": 100

        },

        metadata={

            "type": "analysis"

        }

    )


    assert result.tool == "analytics"

    assert result.success is True

    assert result.data["records"] == 100

    assert (
        result.metadata["type"]
        == "analysis"
    )



def test_tool_result_failure():

    result = ToolResult(

        tool="analytics",

        success=False,

        data={

            "error": "Execution failed"

        },

        metadata={}

    )


    assert result.tool == "analytics"

    assert result.success is False

    assert (
        "error"
        in result.data
    )