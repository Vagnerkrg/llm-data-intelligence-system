class RAGPromptTemplate:
    """
    Builds prompts used by the RAG pipeline.
    """



    def build(
        self,
        context: str,
        question: str
    ) -> str:
        """
        Creates the final prompt for the LLM.
        """


        return f"""
You are an AI assistant specialized in analyzing business data.

Use only the provided context to answer the question.

If the answer is not available in the context,
say that the information was not found.

Context:
{context}


Question:
{question}


Answer:
"""