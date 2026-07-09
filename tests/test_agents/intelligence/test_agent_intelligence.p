from src.agents.intelligence.agent_intelligence import AgentIntelligence



def test_agent_intelligence_creation():

    intelligence = AgentIntelligence()


    assert intelligence.reasoning_engine is not None

    assert intelligence.orchestrator is not None



def test_agent_intelligence_process():

    intelligence = AgentIntelligence()


    result = intelligence.process(

        "Analyze customer data."

    )


    assert result.answer is not None



def test_agent_intelligence_confidence():

    intelligence = AgentIntelligence()


    result = intelligence.process(

        "Test request."

    )


    assert result.confidence is not None



def test_agent_intelligence_metadata():

    intelligence = AgentIntelligence()


    result = intelligence.process(

        "Metadata test."

    )


    assert result.metadata["component"] == "agent_intelligence"