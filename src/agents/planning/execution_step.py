"""
Execution Step

Representa uma unidade individual de execução dentro de um plano.

Responsabilidades:
- identificar uma etapa
- definir ação executada
- armazenar descrição
- controlar estado
- armazenar resultado
- controlar dependências

Compatível com:
- ExecutionPlanner
- PlanExecutor
- StepExecutor
- Runtime Agent Flow
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ExecutionStep:
    """
    Representa uma etapa individual de execução.

    O modelo aceita tanto:
        step_id/action

    quanto:

        name

    para manter compatibilidade
    com versões anteriores do planner.
    """

    step_id: Optional[str] = None

    action: Optional[str] = None

    description: Optional[str] = None

    parameters: Dict[str, Any] = field(default_factory=dict)

    dependencies: List[str] = field(default_factory=list)

    status: str = "pending"

    result: Any = None

    error: Optional[str] = None

    def __post_init__(self):
        """
        Normaliza compatibilidade entre
        name/action/step_id.
        """

        if self.step_id is None and self.action:
            self.step_id = self.action

        if self.action is None and self.step_id:
            self.action = self.step_id

    @property
    def name(self) -> str:
        """
        Compatibilidade com planners antigos.
        """

        return self.step_id

    def mark_running(self):
        """
        Marca execução iniciada.
        """

        self.status = "running"

    def mark_completed(self, result: Any = None):
        """
        Marca execução concluída.
        """

        self.status = "completed"
        self.result = result

    def mark_failed(self, error: str):
        """
        Marca execução falhou.
        """

        self.status = "failed"
        self.error = error

    def is_completed(self) -> bool:
        """
        Verifica conclusão.
        """

        return self.status == "completed"

    def is_failed(self) -> bool:
        """
        Verifica falha.
        """

        return self.status == "failed"

    def can_execute(self, completed_steps: List[str]) -> bool:
        """
        Verifica dependências.
        """

        return all(dependency in completed_steps for dependency in self.dependencies)

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialização.
        """

        return {
            "step_id": self.step_id,
            "action": self.action,
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "dependencies": self.dependencies,
            "status": self.status,
            "result": self.result,
            "error": self.error,
        }
