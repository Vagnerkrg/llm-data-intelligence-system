from typing import List, Dict, Any

from .learning_pattern import LearningPattern


class PatternDetector:
    """
    Responsável por identificar padrões
    em experiências cognitivas.

    Nesta primeira versão o detector trabalha
    com regras simples de similaridade.
    """

    def __init__(self):
        self.patterns: Dict[str, LearningPattern] = {}

    def detect(
        self, pattern_id: str, description: str, metadata: Dict[str, Any] | None = None
    ) -> LearningPattern:
        """
        Detecta ou atualiza um padrão existente.
        """

        if metadata is None:
            metadata = {}

        if pattern_id in self.patterns:
            pattern = self.patterns[pattern_id]

            pattern.increase_frequency()
            pattern.strengthen(0.05)

            return pattern

        pattern = LearningPattern(
            pattern_id=pattern_id,
            description=description,
            frequency=1,
            confidence=0.5,
            metadata=metadata,
        )

        self.patterns[pattern_id] = pattern

        return pattern

    def get_patterns(self) -> List[LearningPattern]:
        """
        Retorna todos os padrões identificados.
        """

        return list(self.patterns.values())

    def count(self) -> int:
        """
        Quantidade de padrões conhecidos.
        """

        return len(self.patterns)
