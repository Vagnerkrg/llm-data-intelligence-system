class AgentRouter:
    """
    Responsible for deciding which tool
    should handle a user request.
    """


    def route(
        self,
        question: str
    ):
        """
        Route a question to the
        appropriate tool name.
        """

        text = question.lower()


        analytical_keywords = [

            "quantos",

            "categoria",

            "colunas",

            "dados",

            "produtos",

            "clientes"

        ]


        if any(
            keyword in text
            for keyword in analytical_keywords
        ):

            return "analytics"


        return None