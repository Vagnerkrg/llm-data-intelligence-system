"""Learning engine service."""

from ..contracts import LearningRequest
from ..domain import LearningOutcome
from .learning_analyzer import LearningAnalyzer
from .learning_extractor import LearningExtractor
from .learning_validator import LearningValidator


class LearningEngine:
    """Core learning execution engine."""

    def __init__(
        self,
        analyzer: LearningAnalyzer | None = None,
        extractor: LearningExtractor | None = None,
        validator: LearningValidator | None = None,
    ) -> None:
        self._analyzer = analyzer or LearningAnalyzer()
        self._extractor = extractor or LearningExtractor()
        self._validator = validator or LearningValidator()

    def learn(
        self,
        request: LearningRequest,
    ) -> list[LearningOutcome]:
        """Execute learning cycle."""

        self._analyzer.analyze(
            request.context
        )

        outcomes = self._extractor.extract(
            request.context.experiences
        )

        if not self._validator.validate(outcomes):
            raise ValueError(
                "Invalid learning outcomes."
            )

        return outcomes