"""Reflection type definitions."""

from enum import Enum


class ReflectionType(str, Enum):
    """Supported reflection categories."""

    PERFORMANCE = "performance"
    STRATEGY = "strategy"
    EXECUTION = "execution"
    DECISION = "decision"
    ADAPTATION = "adaptation"
    KNOWLEDGE = "knowledge"