from typing import Dict, Any


class AnswerGenerator:
    """
    Converts internal system results
    into user-friendly responses.

    Supports:
    - analytical results
    - RAG textual answers
    """


    def generate(
        self,
        result: Any
    ) -> str:
        """
        Generates natural language responses.
        """


        if not result:

            return (
                "Não encontrei informações "
                "suficientes para responder."
            )



        # RAG already generated response

        if isinstance(
            result,
            str
        ):

            return result



        if not isinstance(
            result,
            dict
        ):

            return str(result)



        operation = result.get(
            "operation"
        )



        if operation == "count_rows":

            dataset = result.get(
                "dataset"
            )

            value = result.get(
                "result"
            )


            return (
                f"O dataset {dataset} "
                f"possui {value} registros."
            )



        if operation == "columns":

            columns = result.get(
                "result",
                []
            )


            return (
                "As colunas disponíveis são: "
                +
                ", ".join(columns)
            )



        if operation == "value_counts":

            values = result.get(
                "result",
                {}
            )


            if values:

                category = max(
                    values,
                    key=values.get
                )


                return (
                    f"A categoria com maior "
                    f"quantidade de produtos é "
                    f"'{category}', com "
                    f"{values[category]} registros."
                )



        # Generic fallback

        return (
            "Resultado encontrado: "
            +
            str(result)
        )