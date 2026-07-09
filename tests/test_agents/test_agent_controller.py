from src.agents.agent_controller import AgentController


def test_agent_controller_uses_analytics_tool():

    controller = AgentController()


    response = controller.run(
        "quantos produtos existem?"
    )


    assert response["status"] == "success"

    assert response["tool"] == "analytics"

    assert "result" in response