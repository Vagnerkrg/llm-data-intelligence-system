"""Learning repository service."""


class LearningRepository:
    """Stores learned knowledge."""

    def __init__(self):
        self.storage = []

    def save(self, item):
        """Store learning item."""

        self.storage.append(item)

    def get_all(self):
        """Return stored items."""

        return self.storage

    def count(self) -> int:
        """Return number of stored learning items."""

        return len(self.storage)