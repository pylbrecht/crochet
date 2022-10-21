import uuid
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Iterable

from crochet.domain.events import Event


class IEventStore(ABC):
    @abstractmethod
    def append(self, event: Event):
        pass

    @abstractmethod
    def load_event_stream(self, stream_id: uuid.UUID) -> Iterable[Event]:
        pass


class MemoryEventStore(IEventStore):
    def __init__(self):
        self._store: defaultdict[uuid.UUID, list[Event]] = defaultdict(list)

    def _next_version(self, stream_id: uuid.UUID) -> int:
        last_version = max(
            (event.version for event in self._store[stream_id]), default=0
        )
        return last_version + 1

    def append(self, event: Event):
        if event.version != self._next_version(event.stream_id):
            raise ValueError(
                f"expected version: {self._next_version(event.stream_id)}, "
                f"got {event.version}"
            )

        self._store[event.stream_id].append(event)

    def load_event_stream(self, stream_id: uuid.UUID) -> Iterable[Event]:
        return (event for event in self._store[stream_id])

    def __contains__(self, event: Event):
        if not isinstance(event, Event):
            raise TypeError(f"unsupported type: {type(event)}")

        return event.stream_id in self._store
