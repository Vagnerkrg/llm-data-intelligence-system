from datetime import datetime

from src.agents.evaluation.routing_feedback import RoutingFeedback



def test_routing_feedback_creation():

    feedback = RoutingFeedback(

        question="Quantos produtos existem?",

        selected_tool="analytics",

        successful=True,

        confidence=0.9,

        comment="Correct tool selected.",

        timestamp=datetime.now()

    )


    assert feedback.question == (
        "Quantos produtos existem?"
    )

    assert feedback.selected_tool == (
        "analytics"
    )

    assert feedback.successful is True

    assert feedback.confidence == 0.9

    assert feedback.comment == (
        "Correct tool selected."
    )

    assert isinstance(
        feedback.timestamp,
        datetime
    )



def test_routing_feedback_failed_decision():

    feedback = RoutingFeedback(

        question="Explique uma teoria",

        selected_tool=None,

        successful=False,

        confidence=0.0,

        comment="No suitable tool found.",

        timestamp=datetime.now()

    )


    assert feedback.selected_tool is None

    assert feedback.successful is False

    assert feedback.confidence == 0.0