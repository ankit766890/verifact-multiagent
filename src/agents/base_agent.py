from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple
import time
from src.models.schemas import PipelineExecutionMetric


class BaseAgent(ABC):
    """Abstract Base Class for all autonomous agents in the multi-agent pipeline."""

    def __init__(self, name: str, role_description: str):
        self.name = name
        self.role_description = role_description

    @abstractmethod
    def execute(self, payload: Any, context: Dict[str, Any]) -> Any:
        """Core execution method each agent must implement."""
        pass

    def run_with_telemetry(self, payload: Any, context: Dict[str, Any]) -> Tuple[Any, PipelineExecutionMetric]:
        """Runs the agent with precision execution telemetry and error containment."""
        start_time = time.perf_counter()
        status = "SUCCESS"
        items_count = 1
        try:
            result = self.execute(payload, context)
            if isinstance(result, list):
                items_count = len(result)
            return result, PipelineExecutionMetric(
                agent_name=self.name,
                duration_ms=round((time.perf_counter() - start_time) * 1000, 2),
                status=status,
                items_processed=items_count
            )
        except Exception as e:
            status = f"ERROR: {str(e)}"
            metric = PipelineExecutionMetric(
                agent_name=self.name,
                duration_ms=round((time.perf_counter() - start_time) * 1000, 2),
                status=status,
                items_processed=0
            )
            raise RuntimeError(f"Agent {self.name} failed during task execution: {str(e)}") from e
