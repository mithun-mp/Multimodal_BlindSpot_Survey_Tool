"""
Thread-safe Event Streaming System for BlindSpot.
Enables real-time progress updates, live logging, and UI observability during audits.
"""
from dataclasses import dataclass, field
import threading
import time
import uuid
from typing import Dict, List, Callable, Any, Optional


@dataclass
class ExecutionEvent:
    """Event emitted during pipeline or background audit execution."""
    event_type: str
    data: Dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "data": self.data,
            "timestamp": self.timestamp,
        }


class EventEmitter:
    """Thread-safe event dispatcher and event history buffer."""
    def __init__(self, max_history: int = 1000):
        self._lock = threading.RLock()
        self._listeners: Dict[str, List[Callable[[ExecutionEvent], None]]] = {}
        self._global_listeners: List[Callable[[ExecutionEvent], None]] = []
        self._history: List[ExecutionEvent] = []
        self._max_history = max_history

    def on(self, event_type: str, callback: Callable[[ExecutionEvent], None]) -> None:
        """Register a callback for a specific event type."""
        with self._lock:
            if event_type not in self._listeners:
                self._listeners[event_type] = []
            if callback not in self._listeners[event_type]:
                self._listeners[event_type].append(callback)

    def on_any(self, callback: Callable[[ExecutionEvent], None]) -> None:
        """Register a callback for all emitted events."""
        with self._lock:
            if callback not in self._global_listeners:
                self._global_listeners.append(callback)

    def off(self, event_type: str, callback: Callable[[ExecutionEvent], None]) -> None:
        """Unregister a callback."""
        with self._lock:
            if event_type in self._listeners and callback in self._listeners[event_type]:
                self._listeners[event_type].remove(callback)
            if callback in self._global_listeners:
                self._global_listeners.remove(callback)

    def emit(self, event_type: str, **data: Any) -> ExecutionEvent:
        """Emit an event to all matching listeners and append to history."""
        event = ExecutionEvent(event_type=event_type, data=data)
        callbacks_to_invoke = []

        with self._lock:
            self._history.append(event)
            if len(self._history) > self._max_history:
                self._history.pop(0)

            # Snapshot listeners inside lock
            specific = list(self._listeners.get(event_type, []))
            globals_ = list(self._global_listeners)
            callbacks_to_invoke = specific + globals_

        # Invoke callbacks outside lock to prevent deadlocks
        for cb in callbacks_to_invoke:
            try:
                cb(event)
            except Exception as e:
                # Listener failure should not break event dispatching
                pass

        return event

    def get_history(self, event_type: Optional[str] = None) -> List[ExecutionEvent]:
        """Retrieve copy of logged events."""
        with self._lock:
            if event_type:
                return [e for e in self._history if e.event_type == event_type]
            return list(self._history)

    def clear_history(self) -> None:
        with self._lock:
            self._history.clear()
