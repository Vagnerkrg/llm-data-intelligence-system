from dataclasses import dataclass


@dataclass
class LatencyMetrics:
    """
    Métricas relacionadas ao tempo de execução.
    """

    execution_id: str

    latency_ms: float


    @property
    def latency_seconds(self) -> float:
        return self.latency_ms / 1000