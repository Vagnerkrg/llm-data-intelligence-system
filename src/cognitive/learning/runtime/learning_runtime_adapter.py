from typing import Dict, Any

from ..integration.cognitive_learning_orchestrator import (
    CognitiveLearningOrchestrator
)

from .learning_execution_context import (
    LearningExecutionContext
)



class LearningRuntimeAdapter:
    """
    Adapter responsável por conectar
    o Agent Runtime com o sistema
    cognitivo de aprendizagem.
    """


    def __init__(
        self,
        learning_orchestrator:
            CognitiveLearningOrchestrator
    ):

        self.learning_orchestrator = (
            learning_orchestrator
        )



    def process_feedback(
        self,
        execution_id: str,
        feedback: Dict[str, Any]
    ) -> LearningExecutionContext:
        """
        Processa feedback vindo do runtime.
        """

        context = LearningExecutionContext(
            execution_id=execution_id
        )


        context.add_feedback(
            feedback
        )


        result = (
            self.learning_orchestrator
            .process_learning(feedback)
        )


        if result.get("learned"):

            context.mark_learned(
                result["knowledge_id"]
            )


        return context



    def can_learn(
        self,
        context: LearningExecutionContext
    ) -> bool:
        """
        Verifica se contexto gerou aprendizado.
        """

        return context.has_learning()