import os

from src.llm.groq_client import GroqClient
from src.llm.mock_client import MockLLMClient


class LLMFactory:
    """
    Factory responsible for creating LLM clients.

    Selects the appropriate implementation
    based on environment configuration.
    """


    @staticmethod
    def create():
        """
        Creates an LLM client instance.

        Returns:
            GroqClient when GROQ_API_KEY exists.
            MockLLMClient otherwise.
        """

        api_key = os.getenv(
            "GROQ_API_KEY"
        )


        if api_key:
            return GroqClient()


        return MockLLMClient()