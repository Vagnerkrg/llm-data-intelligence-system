from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any


@dataclass
class LearningExecutionContext:
    """
    Contexto de execução utilizado durante
    processos de aprendizagem cognitiva.

    Mantém identidade da execução,
    feedback recebido e informações
    geradas pelo ciclo de aprendizagem.
    """

    execution_id: str

    feedback: Dict[str, Any] = field(
        default_factory=dict
    )

    learned: bool = False

    knowledge_id: str | None = None

    created_at: datetime = field(
        default_factory=datetime.now
    )


    def mark_learned(
        self,
        knowledge_id: str
    ) -> None:
        """
        Marca execução como aprendizado concluído.
        """

        self.learned = True

        self.knowledge_id = knowledge_id



    def add_feedback(
        self,
        feedback: Dict[str, Any]
    ) -> None:
        """
        Atualiza feedback associado
        à execução.
        """

        self.feedback = feedback



    def has_learning(
        self
    ) -> bool:
        """
        Verifica se houve aprendizado.
        """

        return self.learned