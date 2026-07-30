from src.cognitive.evaluation.feedback_loop.runtime.cognitive_feedback_handler import (
    CognitiveFeedbackHandler,
)

from src.cognitive.evaluation.feedback_loop.runtime.runtime_feedback_context import (
    RuntimeFeedbackContext,
)

from src.cognitive.evaluation.feedback_loop.services.feedback_loop_engine import (
    FeedbackLoopEngine,
)


class FeedbackRuntime:
    """
    Runtime responsável por conectar:

    Execution
        |
        v
    Feedback
        |
        v
    Cognitive Loop
    """

    def __init__(self):

        self.handler = CognitiveFeedbackHandler()
        self.engine = FeedbackLoopEngine()


    def execute_feedback_cycle(
        self,
        context: RuntimeFeedbackContext,
    ):

        feedback = self.handler.handle(
            context
        )

        cycle = self.engine.process_feedback(
            feedback
        )

        return cycle