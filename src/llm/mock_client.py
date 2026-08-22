from src.llm.llm_client import LLMClient


class MockLLMClient(LLMClient):
    """
    Mock LLM implementation used for tests.

    Avoids external API dependency during CI execution.
    """

    def generate(self, prompt: str) -> str:
        """
        Generates deterministic mock responses.
        """

        return "Mock LLM response generated for validation."
