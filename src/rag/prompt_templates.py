class RAGPromptTemplate:
    """
    Builds prompts used by the RAG pipeline.

    Responsible only for creating the final prompt
    that will be sent to the language model.
    """

    def build(
        self,
        context: str,
        question: str
    ) -> str:
        """
        Creates the final prompt for the LLM.

        Args:
            context: Retrieved information from the RAG pipeline.
            question: User question.

        Returns:
            Formatted prompt for the language model.
        """

        return f"""
You are an AI assistant specialized in analyzing business data.

Your task is to answer questions using only the provided context.

Follow these rules:

- Answer in Portuguese.
- Use only information available in the context.
- Do not use external knowledge.
- Do not make assumptions.
- Do not invent data.
- If the answer cannot be found in the context,
  clearly state that the information was not found.

Context:
{context}

Question:
{question}

Answer:
"""