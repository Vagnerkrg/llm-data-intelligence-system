from typing import List, Dict, Any


class KnowledgeExtractor:
    """
    Extrai unidades de conhecimento a partir de padrões cognitivos.

    Responsabilidade:

    - receber padrões identificados;
    - transformar padrões em conhecimento candidato;
    - calcular confiança inicial;
    - preparar conhecimento para consolidação futura.
    """

    def __init__(self):

        self.knowledge = []


    def extract(
        self,
        patterns: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Converte padrões em candidatos de conhecimento.

        Args:
            patterns:
                Lista de padrões extraídos.

        Returns:
            Lista de conhecimentos candidatos.
        """

        if not patterns:

            return []


        extracted = []


        for pattern in patterns:

            occurrences = pattern.get(
                "occurrences",
                0
            )


            confidence = self._calculate_confidence(
                occurrences
            )


            knowledge = {

                "topic": pattern.get(
                    "topic",
                    "unknown"
                ),

                "content": self._build_content(
                    pattern
                ),

                "examples": pattern.get(
                    "examples",
                    []
                ),

                "occurrences": occurrences,

                "confidence": confidence
            }


            extracted.append(
                knowledge
            )


        self.knowledge = extracted


        return extracted



    def _calculate_confidence(
        self,
        occurrences: int
    ) -> float:
        """
        Calcula confiança inicial baseada
        na frequência do padrão.

        Limite máximo: 1.0
        """

        if occurrences <= 0:

            return 0.0


        confidence = occurrences / 10


        return min(
            confidence,
            1.0
        )



    def _build_content(
        self,
        pattern: Dict[str, Any]
    ) -> str:
        """
        Gera uma descrição textual
        do conhecimento extraído.
        """

        topic = pattern.get(
            "topic",
            "general"
        )


        return (
            f"Recurring cognitive pattern "
            f"identified for topic: {topic}"
        )