from typing import List, Optional

from .memory_index import MemoryIndex


class KnowledgeRetriever:
    """
    Responsável por recuperar conhecimentos
    armazenados no sistema de memória cognitiva.

    Suporta:

    - recuperação por id
    - busca por metadados
    - busca textual por conteúdo
    """

    def __init__(self, memory_index: MemoryIndex):

        self.memory_index = memory_index

    def retrieve(self, memory_id: str) -> Optional[dict]:
        """
        Recupera uma memória específica.
        """

        return self.memory_index.get(memory_id)

    def search(self, key: str, value: Optional[str] = None) -> List[dict]:
        """
        Busca conhecimentos armazenados.

        Modos suportados:

        1. Busca por metadado:

            search(
                "type",
                "learning"
            )

        2. Busca textual:

            search(
                "planning"
            )
        """

        results = []

        for memory_id in self.memory_index.list_ids():
            memory = self.memory_index.get(memory_id)

            if memory is None:
                continue

            # -----------------------------
            # Busca por chave/valor
            # -----------------------------

            if value is not None:
                if memory.get(key) == value:
                    results.append({"memory_id": memory_id, "metadata": memory})

            # -----------------------------
            # Busca textual
            # -----------------------------

            else:
                content = str(memory.get("content", ""))

                if key.lower() in content.lower():
                    results.append({"memory_id": memory_id, "content": content})

        return results

    def exists(self, memory_id: str) -> bool:
        """
        Verifica existência de conhecimento.
        """

        return self.memory_index.exists(memory_id)
