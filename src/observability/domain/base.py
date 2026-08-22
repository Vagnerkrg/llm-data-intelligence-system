"""Base serialization contract for observability domain objects."""

from __future__ import annotations

from typing import Any, Dict, Type, TypeVar

from pydantic import BaseModel


ModelT = TypeVar("ModelT", bound="SerializableModel")


class SerializableModel(BaseModel):
    """Base model with explicit serialization helpers."""

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the model to a JSON-compatible dictionary."""
        return self.model_dump(mode="json")

    def to_json(self) -> str:
        """Serialize the model to JSON."""
        return self.model_dump_json()

    @classmethod
    def from_dict(
        cls: Type[ModelT],
        payload: Dict[str, Any],
    ) -> ModelT:
        """Deserialize a model from a dictionary."""
        return cls.model_validate(payload)

    @classmethod
    def from_json(
        cls: Type[ModelT],
        payload: str,
    ) -> ModelT:
        """Deserialize a model from JSON."""
        return cls.model_validate_json(payload)
