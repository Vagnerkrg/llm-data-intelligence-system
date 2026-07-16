"""Learning manager service."""

from ..contracts import LearningRequest, LearningResponse


class LearningManager:
    """Coordinates learning workflow."""

    def __init__(self):
        self.history = []

    def learn(
        self,
        request: LearningRequest | None = None,
    ) -> LearningResponse:
        """Execute learning process."""

        if request is None:
            return LearningResponse(
                success=True,
                result=None,
                message="Learning executed without input",
            )

        self.history.append(request)

        return LearningResponse(
            success=True,
            result=request,
            message="Learning completed",
        )