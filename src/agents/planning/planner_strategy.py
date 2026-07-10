class PlannerStrategy:
    """
    Strategy layer responsible for
    identifying the intent of a user request.

    This component prepares information
    that will be used by the ExecutionPlanner
    to create dynamic execution plans.
    """

    def analyze(
        self,
        question: str
    ) -> dict:
        """
        Analyze user question and classify
        the request type.
        """

        text = question.lower()


        if any(
            keyword in text
            for keyword in [
                "produto",
                "dataset",
                "dados",
                "quantos",
                "quantidade",
                "análise",
                "analise"
            ]
        ):

            return {

                "type": "analytics"

            }



        if any(
            keyword in text
            for keyword in [
                "documento",
                "pdf",
                "arquivo",
                "texto",
                "explique",
                "resuma"
            ]
        ):

            return {

                "type": "document"

            }



        return {

            "type": "unknown"

        }