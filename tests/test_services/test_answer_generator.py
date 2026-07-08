from src.services.answer_generator import AnswerGenerator



class TestAnswerGenerator:
    """
    Tests for AnswerGenerator service.
    """


    def setup_method(self):
        """
        Creates a fresh generator instance
        before each test.
        """

        self.generator = AnswerGenerator()



    def test_generate_count_rows_response(self):
        """
        Validates dataset row count responses.
        """

        result = {
            "operation": "count_rows",
            "dataset": "products",
            "result": 32951
        }


        response = self.generator.generate(
            result
        )


        assert (
            response
            ==
            "O dataset products possui 32951 registros."
        )



    def test_generate_value_counts_response(self):
        """
        Validates category frequency responses.
        """

        result = {
            "operation": "value_counts",
            "dataset": "products",
            "result": {
                "cama_mesa_banho": 3029,
                "esporte_lazer": 2867,
                "moveis_decoracao": 2657
            }
        }


        response = self.generator.generate(
            result
        )


        assert (
            response
            ==
            "A categoria com maior quantidade de produtos é 'cama_mesa_banho', com 3029 registros."
        )



    def test_generate_columns_response(self):
        """
        Validates column listing responses.
        """

        result = {
            "operation": "columns",
            "dataset": "products",
            "result": [
                "product_id",
                "product_category_name"
            ]
        }


        response = self.generator.generate(
            result
        )


        assert (
            response
            ==
            "As colunas disponíveis são: product_id, product_category_name"
        )



    def test_generate_empty_result_response(self):
        """
        Validates empty input handling.
        """

        response = self.generator.generate(
            {}
        )


        assert (
            response
            ==
            "Não encontrei informações suficientes para responder."
        )