import os

from dotenv import load_dotenv
from llama_index.llms.groq import Groq

from src.llm.llm_client import LLMClient


load_dotenv()


class GroqClient(LLMClient):
    """
    Groq implementation of the LLM client.
    """


    def __init__(
        self,
        model="llama-3.1-8b-instant"
    ):

        api_key = os.getenv(
            "GROQ_API_KEY"
        )

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found in environment variables."
            )


        self.llm = Groq(
            model=model,
            api_key=api_key,
            temperature=0
        )


    def generate(
        self,
        prompt: str
    ) -> str:
        """
        Generates a response using Groq.
        """

        response = self.llm.complete(
            prompt
        )


        if not response.text:
            return (
                "Não foi possível gerar uma resposta."
            )


        return response.text