"""API routes."""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from src.api.dependencies import (
    get_cognitive_state_service,
    get_execution_service,
    get_execution_trace_service,
    get_intelligence_system,
    get_learning_evolution_service,
    get_memory_knowledge_service,
)
from src.api.schemas import (
    AnswerResponse,
    CognitiveStateResponse,
    CreateExecutionRequest,
    ExecutionResponse,
    ExecutionTraceResponse,
    EvolutionResponse,
    KnowledgeResponse,
    LearningResponse,
    MemoryResponse,
    QuestionRequest,
)
from src.application.cognitive_state_service import (
    CognitiveStateApplicationService,
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
from src.application.learning_evolution_service import (
    LearningEvolutionApplicationService,
)
from src.application.memory_knowledge_service import (
    MemoryKnowledgeApplicationService,
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


# ---------------------------------------------------------------------------
# Cognitive State API
# ---------------------------------------------------------------------------


@router.get(
    "/api/v1/executions/{execution_id}/cognitive-state",
    response_model=CognitiveStateResponse,
    status_code=status.HTTP_200_OK,
    summary="Get cognitive execution state",
    tags=["cognitive"],
)
def get_cognitive_state(
    execution_id: str,
    service: CognitiveStateApplicationService = Depends(
        get_cognitive_state_service,
    ),
) -> CognitiveStateResponse:
    """Return the consolidated public cognitive state."""
    _validate_execution_id(
        execution_id,
    )

    try:
        return service.get_state(
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
                "error": "COGNITIVE_STATE_UNAVAILABLE",
                "message": str(exc),
            },
        ) from exc


# ---------------------------------------------------------------------------
# Memory & Knowledge API
# ---------------------------------------------------------------------------


@router.get(
    "/api/v1/executions/{execution_id}/memory",
    response_model=MemoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get execution memory observations",
    tags=["memory"],
)
def get_execution_memory(
    execution_id: str,
    service: MemoryKnowledgeApplicationService = Depends(
        get_memory_knowledge_service,
    ),
) -> MemoryResponse:
    """Return public Memory observations for an execution."""
    _validate_execution_id(
        execution_id,
    )

    try:
        return service.get_memory(
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
                "error": "MEMORY_UNAVAILABLE",
                "message": str(exc),
            },
        ) from exc


@router.get(
    "/api/v1/executions/{execution_id}/knowledge",
    response_model=KnowledgeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get execution knowledge observations",
    tags=["knowledge"],
)
def get_execution_knowledge(
    execution_id: str,
    service: MemoryKnowledgeApplicationService = Depends(
        get_memory_knowledge_service,
    ),
) -> KnowledgeResponse:
    """Return public Knowledge observations for an execution."""
    _validate_execution_id(
        execution_id,
    )

    try:
        return service.get_knowledge(
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
                "error": "KNOWLEDGE_UNAVAILABLE",
                "message": str(exc),
            },
        ) from exc


# ---------------------------------------------------------------------------
# Learning & Evolution API
# ---------------------------------------------------------------------------


@router.get(
    "/api/v1/executions/{execution_id}/learning",
    response_model=LearningResponse,
    status_code=status.HTTP_200_OK,
    summary="Get execution learning state",
    tags=["learning"],
)
def get_execution_learning(
    execution_id: str,
    service: LearningEvolutionApplicationService = Depends(
        get_learning_evolution_service,
    ),
) -> LearningResponse:
    """Return public Cognitive Learning observations."""
    _validate_execution_id(
        execution_id,
    )

    try:
        return service.get_learning(
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
                "error": "LEARNING_UNAVAILABLE",
                "message": str(exc),
            },
        ) from exc


@router.get(
    "/api/v1/executions/{execution_id}/evolution",
    response_model=EvolutionResponse,
    status_code=status.HTTP_200_OK,
    summary="Get execution evolution state",
    tags=["evolution"],
)
def get_execution_evolution(
    execution_id: str,
    service: LearningEvolutionApplicationService = Depends(
        get_learning_evolution_service,
    ),
) -> EvolutionResponse:
    """Return public Autonomous Evolution observations."""
    _validate_execution_id(
        execution_id,
    )

    try:
        return service.get_evolution(
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
                "error": "EVOLUTION_UNAVAILABLE",
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
