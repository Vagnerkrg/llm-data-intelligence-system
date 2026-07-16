from dataclasses import dataclass


@dataclass
class KnowledgeContext:
    """
    Context information associated with
    generated knowledge.
    """

    source: str

    domain: str