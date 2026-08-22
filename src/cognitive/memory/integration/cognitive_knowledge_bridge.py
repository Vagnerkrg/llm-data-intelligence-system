"""
Cognitive Knowledge Bridge

Responsável por conectar o conhecimento consolidado
com a camada de memória cognitiva.

Fluxo:

Learning Memory
        |
        v
Consolidation Pipeline
        |
        v
Consolidated Knowledge
        |
        v
Cognitive Knowledge Bridge
        |
        v
Knowledge Retrieval
        |
        v
Future Agent Improvement
"""

from typing import List, Dict, Any

from src.cognitive.memory.consolidation.consolidated_knowledge import (
    ConsolidatedKnowledge,
)


class CognitiveKnowledgeBridge:
    """
    Ponte entre conhecimento consolidado
    e memória cognitiva reutilizável.
    """

    def __init__(self):
        self.knowledge_store: List[ConsolidatedKnowledge] = []

    def add_knowledge(self, knowledge: ConsolidatedKnowledge) -> ConsolidatedKnowledge:
        """
        Adiciona conhecimento consolidado
        ao repositório cognitivo.
        """

        self.knowledge_store.append(knowledge)

        return knowledge

    def consolidate(
        self, knowledge_items: List[ConsolidatedKnowledge]
    ) -> List[ConsolidatedKnowledge]:
        """
        Recebe conhecimento consolidado
        e registra na memória cognitiva.
        """

        for knowledge in knowledge_items:
            self.add_knowledge(knowledge)

        return self.knowledge_store

    def retrieve(self, knowledge_id: str) -> ConsolidatedKnowledge | None:
        """
        Recupera conhecimento pelo identificador.
        """

        for knowledge in self.knowledge_store:
            if knowledge.id == knowledge_id:
                return knowledge

        return None

    def exists(self, knowledge_id: str) -> bool:
        """
        Verifica existência de conhecimento.
        """

        return self.retrieve(knowledge_id) is not None

    def count(self) -> int:
        """
        Retorna quantidade de conhecimentos armazenados.
        """

        return len(self.knowledge_store)

    def search(self, term: str) -> List[ConsolidatedKnowledge]:
        """
        Busca simples por conteúdo.
        """

        results = []

        term_lower = term.lower()

        for knowledge in self.knowledge_store:
            content = str(knowledge.content).lower()

            if term_lower in content:
                results.append(knowledge)

        return results

    def export_metadata(self) -> List[Dict[str, Any]]:
        """
        Exporta metadados do conhecimento.
        """

        metadata = []

        for knowledge in self.knowledge_store:
            metadata.append(
                {
                    "id": knowledge.id,
                    "confidence": knowledge.confidence,
                    "metadata": knowledge.metadata,
                }
            )

        return metadata
