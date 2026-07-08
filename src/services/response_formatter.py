class ResponseFormatter:
    """
    Converts structured analysis results
    into human readable responses.
    """


    def format(
        self,
        result
    ):

        if result.get("operation") == "count_rows":

            return (
                f"O dataset {result['dataset']} "
                f"possui {result['result']} registros."
            )


        if result.get("operation") == "value_counts":

            values = result["result"]

            first_item = next(
                iter(values.items())
            )


            category, amount = first_item


            return (
                f"A categoria com maior quantidade "
                f"de produtos é '{category}', "
                f"com {amount} registros."
            )


        if result.get("operation") == "columns":

            columns = ", ".join(
                result["result"]
            )

            return (
                f"As colunas disponíveis são: {columns}."
            )


        return str(result)