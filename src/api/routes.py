"""API routes."""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from src.api.dependencies import (
    get_execution_service,
    get_execution_trace_service,
    get_intelligence_system,
)
from src.api.schemas import (
    AnswerResponse,
    CreateExecutionRequest,
    ExecutionResponse,
    ExecutionTraceResponse,
    QuestionRequest,
)
from src.application.execution_service import (
    ExecutionApplicationService,
)
from src.application.execution_trace_service import (
    ExecutionTraceApplicationService,
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


@router.get(
    "/api/v1/executions/{execution_id}",
    response_model=ExecutionResponse,
    status_code=status.HTTP_200_OK,
    summary="Get execution status and result",
    tags=["execution"],
)
def get_execution(
    execution_id: str,
    service: ExecutionTraceApplicationService = Depends(
        get_execution_trace_service,
    ),
) -> ExecutionResponse:
    """Return a public execution representation."""
    _validate_execution_id(
        execution_id,
    )

    try:
        return service.get_execution(
            execution_id,
        )

    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "EXECUTION_NOT_FOUND",
                "message": str(exc),
            },
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "TRACE_UNAVAILABLE",
                "message": str(exc),
            },
        ) from exc


@router.get(
    "/api/v1/executions/{execution_id}/trace",
    response_model=ExecutionTraceResponse,
    status_code=status.HTTP_200_OK,
    summary="Get complete execution trace",
    tags=["execution"],
)
def get_execution_trace(
    execution_id: str,
    service: ExecutionTraceApplicationService = Depends(
        get_execution_trace_service,
    ),
) -> ExecutionTraceResponse:
    """Return the complete public execution trace."""
    _validate_execution_id(
        execution_id,
    )

    try:
        return service.get_trace(
            execution_id,
        )

    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "TRACE_NOT_FOUND",
                "message": str(exc),
            },
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "TRACE_UNAVAILABLE",
                "message": str(exc),
            },
        ) from exc


def _validate_execution_id(
    execution_id: str,
) -> None:
    """Validate the public execution identifier."""
    if not execution_id.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail={
                "error": "INVALID_EXECUTION_ID",
                "message": "execution_id must not be empty.",
            },
        )
