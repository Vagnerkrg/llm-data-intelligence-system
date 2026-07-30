from typing import Dict, Any


from src.cognitive.memory.integration.learning_memory_bridge import (
    LearningMemoryBridge
)

from src.cognitive.memory.intelligence.knowledge_retriever import (
    KnowledgeRetriever
)


class CognitiveMemoryOrchestrator:
    """
    Orquestrador da memória cognitiva.

    Responsável por coordenar:

    - armazenamento de conhecimento aprendido
    - recuperação de conhecimento específico
    - busca de conhecimento relevante
    - consultas da memória cognitiva

    Atua como camada única de acesso
    para agentes cognitivos.
    """


    def __init__(
        self,
        learning_memory_bridge: LearningMemoryBridge,
        knowledge_retriever: KnowledgeRetriever
    ):
        self.learning_memory_bridge = (
            learning_memory_bridge
        )

        self.knowledge_retriever = (
            knowledge_retriever
        )


    def store_learning(
        self,
        knowledge
    ) -> Dict[str, Any]:
        """
        Armazena conhecimento aprendido
        na memória cognitiva.
        """

        return self.learning_memory_bridge.store_learning(
            knowledge
        )



    def retrieve_learning(
        self,
        knowledge_id: str
    ):
        """
        Recupera conhecimento através
        do identificador.
        """

        return self.learning_memory_bridge.retrieve_learning(
            knowledge_id
        )



    def search_memory(
        self,
        query: str
    ):
        """
        Busca conhecimento relevante
        na memória.

        O KnowledgeRetriever trabalha
        com busca chave/valor, então
        adaptamos a consulta para
        pesquisa por conteúdo.
        """

        return self.knowledge_retriever.search(
            "content",
            query
        )



    def exists(
        self,
        knowledge_id: str
    ) -> bool:
        """
        Verifica se um conhecimento
        existe na memória.
        """

        return self.learning_memory_bridge.exists(
            knowledge_id
        )



    def count(self) -> int:
        """
        Retorna quantidade de memórias
        armazenadas.
        """

        return self.learning_memory_bridge.count()