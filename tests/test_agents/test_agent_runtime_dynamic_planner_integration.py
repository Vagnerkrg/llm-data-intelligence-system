from src.agents.runtime.agent_runtime import AgentRuntime
from src.agents.controller.agent_controller import AgentController
from src.agents.planning.dynamic_execution_planner import DynamicExecutionPlanner


class DynamicPlannerRuntimeController(AgentController):
    """
    Controller configured with DynamicExecutionPlanner
    for runtime integration tests.
    """

    def __init__(self):

        super().__init__()

        self.dynamic_planner = DynamicExecutionPlanner()


    def create_plan(
        self,
        question: str
    ):

        return self.dynamic_planner.create_plan(
            question
        )



def test_agent_runtime_dynamic_planner_integration():

    controller = DynamicPlannerRuntimeController()

    runtime = AgentRuntime(
        controller=controller
    )

    context = runtime.prepare(
        "Analise os dados de vendas e encontre padrões"
    )

    assert context.plan is not None



def test_agent_runtime_dynamic_planner_generates_expected_plan():

    controller = DynamicPlannerRuntimeController()

    runtime = AgentRuntime(
        controller=controller
    )

    context = runtime.prepare(
        "Explique o conteúdo deste documento"
    )

    steps = context.plan.steps

    assert len(
        steps
    ) == 3

    assert steps[0].action == "route_request"
    assert steps[1].action == "execute_tool"
    assert steps[2].action == "generate_response"



def test_agent_runtime_dynamic_planner_supports_multiple_intents():

    controller = DynamicPlannerRuntimeController()

    runtime = AgentRuntime(
        controller=controller
    )

    analytics_context = runtime.prepare(
        "Faça uma análise estatística dos dados"
    )

    document_context = runtime.prepare(
        "Resuma este documento PDF"
    )


    assert analytics_context.plan is not None

    assert document_context.plan is not None

    assert len(
        analytics_context.plan.steps
    ) == len(
        document_context.plan.steps
    )