from src.agents.reasoning.reasoning_result import ReasoningResult



class ReasoningEngine:
    """
    Responsible for generating
    reasoning outputs.

    This layer transforms user requests
    into structured reasoning information
    that can be consumed by planning layers.

    Future versions may integrate
    LLM based reasoning strategies.
    """



    def reason(
        self,
        question: str
    ) -> ReasoningResult:
        """
        Generate structured reasoning
        result from a user request.
        """


        reasoning = (
            f"Analyzing request: {question}"
        )


        conclusion = (
            "Request analyzed successfully."
        )


        intent = self._detect_intent(
            question
        )


        goal = self._define_goal(
            question,
            intent
        )


        capabilities = (
            self._define_capabilities(
                intent
            )
        )


        strategy = (
            self._define_strategy(
                intent
            )
        )


        return ReasoningResult(

            reasoning=reasoning,

            conclusion=conclusion,

            confidence=0.8,

            goal=goal,

            intent=intent,

            required_capabilities=capabilities,

            strategy=strategy,

            metadata={

                "source": "reasoning_engine"

            }

        )



    def _detect_intent(
        self,
        question: str
    ) -> str:
        """
        Basic intent detection.

        Future versions may replace
        this logic with LLM reasoning.
        """

        text = question.lower()


        if any(
            keyword in text
            for keyword in [
                "analisar",
                "análise",
                "analise",
                "venda",
                "produto",
                "dados"
            ]
        ):

            return "analytics"


        if any(
            keyword in text
            for keyword in [
                "buscar",
                "encontrar",
                "pesquisar"
            ]
        ):

            return "search"


        return "general"



    def _define_goal(
        self,
        question: str,
        intent: str
    ) -> str:
        """
        Define the execution goal.
        """

        return (
            f"Resolve user request with intent: {intent}"
        )



    def _define_capabilities(
        self,
        intent: str
    ):
        """
        Define required capabilities
        for execution.
        """

        mapping = {

            "analytics": [
                "data_analysis"
            ],

            "search": [
                "information_retrieval"
            ],

            "general": [
                "general_reasoning"
            ]

        }


        return mapping.get(
            intent,
            []
        )



    def _define_strategy(
        self,
        intent: str
    ) -> str:
        """
        Define initial execution strategy.
        """

        strategies = {

            "analytics":
                "Use analytics tools",

            "search":
                "Use retrieval tools",

            "general":
                "Use general reasoning"

        }


        return strategies.get(
            intent,
            "Use default strategy"
        )
   