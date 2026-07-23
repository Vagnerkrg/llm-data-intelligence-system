class NormalizedStrategy:
    """
    Estratégia responsável por normalizar scores
    de avaliação cognitiva.

    Resultado sempre entre 0.0 e 1.0.
    """

    def evaluate(
        self,
        score: float,
        minimum: float = 0.0,
        maximum: float = 1.0
    ) -> float:
        """
        Normaliza um valor para intervalo [0,1].

        Fórmula:

        (score - minimum) / (maximum - minimum)
        """

        if maximum <= minimum:
            return 0.0

        normalized = (
            (score - minimum)
            /
            (maximum - minimum)
        )

        if normalized < 0:
            return 0.0

        if normalized > 1:
            return 1.0

        return normalized