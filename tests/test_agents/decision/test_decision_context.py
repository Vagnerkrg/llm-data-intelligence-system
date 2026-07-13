from src.agents.decision.decision_context import DecisionContext


def test_should_create_decision_context_with_goal():
    context = DecisionContext(
        goal="Optimize analysis strategy"
    )

    assert context.goal == "Optimize analysis strategy"


def test_should_create_empty_collections_by_default():
    context = DecisionContext(
        goal="Improve execution"
    )

    assert context.constraints == []
    assert context.capabilities == []
    assert context.available_tools == []
    assert context.metadata == {}


def test_should_store_constraints():
    context = DecisionContext(
        goal="Optimize execution",
        constraints=[
            "low_cost",
            "fast_response"
        ],
    )

    assert len(context.constraints) == 2
    assert "low_cost" in context.constraints


def test_should_store_available_capabilities():
    context = DecisionContext(
        goal="Analyze data",
        capabilities=[
            "analytics",
            "retrieval"
        ],
    )

    assert "analytics" in context.capabilities
    assert "retrieval" in context.capabilities


def test_should_store_available_tools():
    context = DecisionContext(
        goal="Generate report",
        available_tools=[
            "analytics_tool",
            "search_tool"
        ],
    )

    assert len(context.available_tools) == 2
    assert "analytics_tool" in context.available_tools


def test_should_store_metadata_information():
    context = DecisionContext(
        goal="Decision analysis",
        metadata={
            "domain": "finance",
            "priority": "high",
        },
    )

    assert context.metadata["domain"] == "finance"
    assert context.metadata["priority"] == "high"


def test_should_support_complete_context_definition():
    context = DecisionContext(
        goal="Select best strategy",
        constraints=[
            "time_limit"
        ],
        capabilities=[
            "reasoning"
        ],
        available_tools=[
            "analytics_tool"
        ],
        metadata={
            "source": "agent_runtime"
        },
    )

    assert context.goal == "Select best strategy"
    assert len(context.constraints) == 1
    assert len(context.capabilities) == 1
    assert len(context.available_tools) == 1
    assert context.metadata["source"] == "agent_runtime"