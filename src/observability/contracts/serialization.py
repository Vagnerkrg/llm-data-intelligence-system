"""Serialization contracts for observability domain models."""

from __future__ import annotations

from typing import Any, Dict, Protocol, TypeVar


SerializableT = TypeVar("SerializableT")


class SerializableContract(Protocol):
    """Contract for serializable domain models."""

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-compatible dictionary."""
        ...

    def to_json(self) -> str:
        """Return a JSON string."""
        ...


class DeserializableContract(Protocol):
    """Contract for deserializable domain models."""

    @classmethod
    def from_dict(
        cls,
        payload: Dict[str, Any],
    ) -> SerializableT:
        """Build a model from a dictionary."""
        ...

    @classmethod
    def from_json(
        cls,
        payload: str,
    ) -> SerializableT:
        """Build a model from JSON."""
        ...
