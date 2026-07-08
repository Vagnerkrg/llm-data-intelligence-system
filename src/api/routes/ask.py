from fastapi import APIRouter, Depends

from src.api.schemas import (
    QuestionRequest,
    AnswerResponse
)

from src.api.dependencies import (
    get_intelligence_system
)

from src.application.intelligence_system import (
    IntelligenceSystem
)


router = APIRouter()



@router.post(
    "/ask",
    response_model=AnswerResponse
)
def ask_question(
    request: QuestionRequest,
    system: IntelligenceSystem = Depends(
        get_intelligence_system
    )
):

    response = system.ask(
        request.question
    )


    return AnswerResponse(

        answer=response.answer,

        source=response.source,

        confidence=response.confidence,

        metadata=response.metadata

    )