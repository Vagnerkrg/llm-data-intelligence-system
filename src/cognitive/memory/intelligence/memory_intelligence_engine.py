from typing import List

from src.cognitive.memory.intelligence.memory_index import (
    MemoryIndex
)

from src.cognitive.memory.intelligence.knowledge_retriever import (
    KnowledgeRetriever
)

from src.cognitive.memory.intelligence.learning_memory_manager import (
    LearningMemoryManager
)



class MemoryIntelligenceEngine:
    """
    Engine central da camada Memory Intelligence.

    Responsável por coordenar:

    - armazenamento de memórias
    - recuperação inteligente
    - busca contextual
    - gerenciamento de aprendizado
    """



    def __init__(self):

        self.memory_index = MemoryIndex()

        self.knowledge_retriever = KnowledgeRetriever(
            self.memory_index
        )

        self.learning_manager = LearningMemoryManager()



    def store(
        self,
        content: str
    ) -> str:
        """
        Armazena uma nova memória.
        """

        memory_id = self.memory_index.add(
            metadata={
                "content": content
            }
        )


        self.learning_manager.store(
            memory_id,
            content
        )


        return memory_id



    def retrieve(
        self,
        memory_id: str
    ):
        """
        Recupera memória pelo identificador.
        """

        return self.memory_index.get(
            memory_id
        )



    def search(
        self,
        query: str
    ) -> List:
        """
        Busca conhecimento relacionado.
        """

        return self.knowledge_retriever.search(
            query
        )



    def count(
        self
    ) -> int:
        """
        Retorna quantidade de memórias.
        """

        return self.memory_index.count()