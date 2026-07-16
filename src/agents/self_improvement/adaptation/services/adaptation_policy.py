class AdaptationPolicy:
    """
    Defines rules that determine whether an adaptation can be applied.
    """

    def evaluate(
        self,
        confidence: float,
    ) -> bool:
        """
        Determines if confidence is enough for adaptation.
        """

        return confidence >= 0.7