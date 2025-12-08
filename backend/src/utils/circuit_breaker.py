import time
import threading
from enum import Enum
from typing import Callable, Any, Optional


class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Tripped, requests blocked
    HALF_OPEN = "half_open" # Testing if failure is resolved


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60, expected_exception: type = Exception):
        self.failure_threshold = failure_threshold  # Number of failures before opening
        self.timeout = timeout  # Time in seconds before attempting reset
        self.expected_exception = expected_exception

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time = None
        self._lock = threading.Lock()

    def call(self, func: Callable, *args, **kwargs) -> Any:
        with self._lock:
            if self._state == CircuitState.OPEN:
                # Check if enough time has passed to try again
                if time.time() - self._last_failure_time >= self.timeout:
                    self._state = CircuitState.HALF_OPEN
                else:
                    raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)

            with self._lock:
                if self._state == CircuitState.HALF_OPEN or self._state == CircuitState.CLOSED:
                    # Success, reset the breaker
                    self._state = CircuitState.CLOSED
                    self._failure_count = 0
                    self._last_failure_time = None

            return result

        except self.expected_exception as e:
            with self._lock:
                self._failure_count += 1
                self._last_failure_time = time.time()

                if self._failure_count >= self.failure_threshold:
                    self._state = CircuitState.OPEN

            raise e

    def state(self) -> CircuitState:
        with self._lock:
            return self._state


# Default circuit breaker instance
default_circuit_breaker = CircuitBreaker()