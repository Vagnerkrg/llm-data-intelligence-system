from abc import ABC, abstractmethod


class LLMClient(ABC):
    """
    Generic interface for Large Language Model clients.

    All LLM providers must implement this contract.
    """


    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generates a response from the language model.

        Parameters:
            prompt:
                User input or instruction.

        Returns:
            Generated text response.
        """

        pass