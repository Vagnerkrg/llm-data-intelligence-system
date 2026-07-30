from typing import List, Dict, Any


class PatternExtractor:
    """
    Extrai padrões recorrentes a partir de experiências armazenadas.

    Responsabilidade:
    - analisar experiências de aprendizado;
    - identificar agrupamentos semelhantes;
    - gerar padrões reutilizáveis.

    Primeira versão:
    - baseada em similaridade simples por campos compartilhados.
    """

    def __init__(self):
        self.patterns = []


    def extract(
        self,
        experiences: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Extrai padrões a partir de experiências.

        Args:
            experiences:
                Lista de experiências cognitivas.

        Returns:
            Lista de padrões identificados.
        """

        if not experiences:
            return []


        grouped = {}


        for experience in experiences:

            key = self._generate_key(
                experience
            )


            if key not in grouped:
                grouped[key] = {
                    "topic": experience.get(
                        "topic"
                    ),
                    "occurrences": 0,
                    "examples": []
                }


            grouped[key]["occurrences"] += 1

            grouped[key]["examples"].append(
                experience
            )


        self.patterns = list(
            grouped.values()
        )


        return self.patterns



    def _generate_key(
        self,
        experience: Dict[str, Any]
    ) -> str:
        """
        Gera chave simples para agrupamento.
        """

        if "topic" in experience:
            return str(
                experience["topic"]
            )


        if "type" in experience:
            return str(
                experience["type"]
            )


        return "general"