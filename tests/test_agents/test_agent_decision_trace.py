from datetime import datetime

from src.agents.observability.agent_decision_trace import AgentDecisionTrace



def test_agent_decision_trace_creation():

    trace = AgentDecisionTrace(

        question="quantos produtos existem?",

        selected_tool="analytics",

        confidence=0.95,

        reason="Matched analytical capability.",

        execution_time=0.25,

        success=True,

        result={
            "total": 100
        },

        timestamp=datetime.now()

    )


    assert trace.question == (
        "quantos produtos existem?"
    )


    assert trace.selected_tool == (
        "analytics"
    )


    assert trace.confidence == 0.95


    assert trace.success is True



def test_agent_decision_trace_without_tool():

    trace = AgentDecisionTrace(

        question="pergunta desconhecida",

        selected_tool=None,

        confidence=0.0,

        reason="No matching tool found.",

        execution_time=0.0,

        success=False,

        result=None,

        timestamp=datetime.now()

    )


    assert trace.selected_tool is None


    assert trace.success is False


    assert trace.result is None