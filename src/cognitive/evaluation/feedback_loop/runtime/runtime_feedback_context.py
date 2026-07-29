from dataclasses import dataclass
from datetime import datetime


@dataclass
class RuntimeFeedbackContext:
    """
    Contexto de execução utilizado
    durante o ciclo de feedback cognitivo.
    """

    execution_id: str
    agent_id: str
    capability: str
    signal: str
    impact: str
    created_at: datetime