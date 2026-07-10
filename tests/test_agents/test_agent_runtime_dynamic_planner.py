from src.agents.runtime.agent_runtime import AgentRuntime
from src.agents.controller.agent_controller import AgentController
from src.agents.planning.dynamic_execution_planner import DynamicExecutionPlanner


class DynamicPlannerController(AgentController):
    """
    Test controller using DynamicExecutionPlanner.
    """

    def __init__(self):

        super().__init__()

        self.planner = DynamicExecutionPlanner()


    def create_plan(
        self,
        question: str
    ):

        return self.planner.create_plan(
            question
        )



def test_agent_runtime_uses_dynamic_planner():

    controller = DynamicPlannerController()

    runtime = AgentRuntime(
        controller=controller
    )

    context = runtime.prepare(
        "Analise os dados de vendas e encontre padrões"
    )

    assert context.plan is not None



def test_agent_runtime_dynamic_planner_creates_execution_flow():

    controller = DynamicPlannerController()

    runtime = AgentRuntime(
        controller=controller
    )

    context = runtime.prepare(
        "Explique o conteúdo deste documento"
    )

    assert context.plan is not None

    assert len(
        context.plan.steps
    ) == 3



def test_agent_runtime_dynamic_planner_contains_expected_steps():

    controller = DynamicPlannerController()

    runtime = AgentRuntime(
        controller=controller
    )

    context = runtime.prepare(
        "Faça uma análise estatística dos dados"
    )

    actions = [
        step.action
        for step in context.plan.steps
    ]

    assert "route_request" in actions
    assert "execute_tool" in actions
    assert "generate_response" in actions