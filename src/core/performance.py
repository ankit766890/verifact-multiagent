import time
import functools
from typing import Dict, Any, Callable, Optional


class PerformanceMonitor:
    """
    High-performance telemetry & caching engine.
    Provides sub-millisecond execution memoization and microsecond precision metrics.
    """
    _cache: Dict[str, Any] = {}
    _max_cache_size: int = 256

    @classmethod
    def get_cached(cls, key: str) -> Optional[Any]:
        return cls._cache.get(key)

    @classmethod
    def set_cache(cls, key: str, value: Any) -> None:
        if len(cls._cache) >= cls._max_cache_size:
            # Evict first inserted key (FIFO)
            first_key = next(iter(cls._cache))
            cls._cache.pop(first_key, None)
        cls._cache[key] = value

    @classmethod
    def clear_cache(cls) -> None:
        cls._cache.clear()

    @staticmethod
    def measure_latency(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            duration = (time.perf_counter() - start) * 1000.0
            return result, round(duration, 3)
        return wrapper
