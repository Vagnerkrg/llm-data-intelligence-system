from ..domain.improvement_result import ImprovementResult
from ..domain.improvement_status import ImprovementStatus


class ImprovementValidator:
    """
    Validates cognitive improvement cycle results.

    Validation rules V1.18:

    - Result must exist
    - Status must indicate completion
    """


    def validate(
        self,
        result: ImprovementResult
    ) -> bool:
        """
        Validate improvement result.
        """

        if result is None:
            return False


        return (
            result.status
            == ImprovementStatus.COMPLETED
        )