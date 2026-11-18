from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple
import time
from src.models.schemas import PipelineExecutionMetric


class BaseAgent(ABC):
    """Abstract Cognitive Agent with performance profiling and telemetry."""

    def __init__(self, name: str, role_description: str):
        self.name = name
        self.role_description = role_description

    @abstractmethod
    def execute(self, payload: Any, context: Dict[str, Any]) -> Any:
        """Execution contract."""
        pass

    def run_with_telemetry(self, payload: Any, context: Dict[str, Any]) -> Tuple[Any, PipelineExecutionMetric]:
        start_time = time.perf_counter()
        status = "SUCCESS"
        items_count = 1
        try:
            result = self.execute(payload, context)
            if isinstance(result, list):
                items_count = len(result)
            duration = round((time.perf_counter() - start_time) * 1000, 2)
            return result, PipelineExecutionMetric(
                agent_name=self.name,
                agent_role=self.role_description,
                duration_ms=duration,
                status=status,
                items_processed=items_count
            )
        except Exception as e:
            duration = round((time.perf_counter() - start_time) * 1000, 2)
            metric = PipelineExecutionMetric(
                agent_name=self.name,
                agent_role=self.role_description,
                duration_ms=duration,
                status=f"ERROR: {str(e)}",
                items_processed=0
            )
            raise RuntimeError(f"Agent {self.name} failed: {str(e)}") from e
