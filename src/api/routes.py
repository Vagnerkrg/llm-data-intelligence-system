"""API routes."""

from fastapi import APIRouter, Depends, status

from src.api.dependencies import (
    get_execution_service,
    get_intelligence_system,
)
from src.api.schemas import (
    AnswerResponse,
    CreateExecutionRequest,
    ExecutionResponse,
    QuestionRequest,
)
from src.application.execution_service import (
    ExecutionApplicationService,
)
from src.application.intelligence_system import (
    IntelligenceSystem,
)


router = APIRouter()


# ---------------------------------------------------------------------------
# Legacy API
# ---------------------------------------------------------------------------


@router.post(
    "/ask",
    response_model=AnswerResponse,
)
def ask_question(
    request: QuestionRequest,
    system: IntelligenceSystem = Depends(
        get_intelligence_system,
    ),
) -> AnswerResponse:
    """Legacy /ask endpoint preserved for backward compatibility."""
    response = system.ask(
        request.question,
    )

    return AnswerResponse(
        answer=response.answer,
        source=response.source,
        confidence=response.confidence,
        metadata=response.metadata,
    )


# ---------------------------------------------------------------------------
# V1 Execution API
# ---------------------------------------------------------------------------


@router.post(
    "/api/v1/ask",
    response_model=ExecutionResponse,
    status_code=status.HTTP_200_OK,
    summary="Execute a cognitive request",
    tags=["execution"],
)
def execute(
    request: CreateExecutionRequest,
    service: ExecutionApplicationService = Depends(
        get_execution_service,
    ),
) -> ExecutionResponse:
    """Execute a query through the public Execution API contract."""
    return service.execute(
        request,
    )
