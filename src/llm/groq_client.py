from src.llm.llm_client import LLMClient


class GroqClient(LLMClient):
    """
    Groq implementation of the LLM client.
    """


    def __init__(self, model):
        self.model = model


    def generate(self, prompt: str) -> str:
        """
        Generates a response using Groq.

        This method will be implemented
        in the next step.
        """

        raise NotImplementedError(
            "Groq generation not implemented yet."
        )