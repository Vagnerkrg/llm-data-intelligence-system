from src.agents.runtime.agent_runtime import AgentRuntime
from src.agents.planning.dynamic_execution_planner import DynamicExecutionPlanner


class MockPlanner:

    def __init__(self):
        self.called = False


    def create_plan(
        self,
        question: str
    ):
        self.called = True

        return DynamicExecutionPlanner().create_plan(
            question
        )



def test_agent_runtime_accepts_custom_planner():

    planner = MockPlanner()

    runtime = AgentRuntime(
        planner=planner
    )

    assert runtime.execution_planner == planner



def test_agent_runtime_uses_injected_planner():

    planner = MockPlanner()

    runtime = AgentRuntime(
        planner=planner
    )


    runtime.create_initial_plan(
        "Analise os dados de vendas"
    )


    assert planner.called is True



def test_agent_runtime_injected_planner_generates_valid_plan():

    planner = MockPlanner()

    runtime = AgentRuntime(
        planner=planner
    )


    plan = runtime.create_initial_plan(
        "Explique este documento"
    )


    assert plan is not None

    assert len(
        plan.steps
    ) > 0