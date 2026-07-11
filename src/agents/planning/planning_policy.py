from typing import List, Dict


class PlanningPolicy:
    """
    Defines planning strategies
    based on goal information.

    V1.12:
    Planning becomes goal driven.

    The policy translates:

    - intent
    - capabilities
    - strategy

    into executable planning steps.
    """



    def get_steps(
        self,
        intent: str,
        required_capabilities: List[str] = None,
        strategy: str = None
    ) -> List[Dict[str, str]]:
        """
        Generate execution steps
        based on goal information.
        """


        required_capabilities = (
            required_capabilities
            if required_capabilities
            else []
        )


        strategy = (
            strategy
            if strategy
            else "default"
        )



        #
        # Analytics planning
        #

        if intent == "analytics":

            return [

                {
                    "action": "analyze_data",

                    "description":
                        "Analyze requested data "
                        "using analytics capabilities."
                },


                {
                    "action": "generate_insights",

                    "description":
                        "Generate insights "
                        "from analysis results."
                }

            ]



        #
        # Search planning
        #

        if intent == "search":

            return [

                {
                    "action": "retrieve_information",

                    "description":
                        "Retrieve relevant "
                        "information."
                },


                {
                    "action": "evaluate_results",

                    "description":
                        "Evaluate retrieved "
                        "information."
                }

            ]



        #
        # General reasoning
        #

        if intent == "general":

            return [

                {
                    "action": "reason_about_request",

                    "description":
                        "Apply general reasoning "
                        "to understand request."
                }

            ]



        #
        # Capability based fallback
        #

        if "data_analysis" in required_capabilities:

            return [

                {
                    "action": "analyze_data",

                    "description":
                        "Execute data analysis."
                }

            ]



        if "information_retrieval" in required_capabilities:

            return [

                {
                    "action": "retrieve_information",

                    "description":
                        "Execute information retrieval."
                }

            ]



        #
        # Default fallback
        #

        return [

            {
                "action": "execute_tool",

                "description":
                    "Execute selected capability."
            }

        ]