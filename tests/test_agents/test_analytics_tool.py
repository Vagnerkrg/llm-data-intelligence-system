from src.agents.tools.analytics_tool import AnalyticsTool



def test_analytics_tool_execution():

    tool = AnalyticsTool()


    response = tool.execute(
        "Quantos produtos existem?"
    )


    assert response["type"] == "analysis"

    assert response["operation"] == "count_rows"

    assert response["dataset"] == "products"



def test_analytics_tool_name():

    tool = AnalyticsTool()


    assert tool.name == "analytics"

    assert "analysis" in tool.description.lower()