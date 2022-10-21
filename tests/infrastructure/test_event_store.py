import uuid

import pytest

from crochet.domain.events import Event
from crochet.infrastructure.event_store import MemoryEventStore


def test_append_event_to_stream():
    class SomeEvent(Event):
        pass

    event = SomeEvent(uuid.uuid4(), version=1)

    event_store = MemoryEventStore()
    event_store.append(event)

    assert event in event_store


def test_append_raises_in_case_of_version_conflict():
    class SomeEvent(Event):
        pass

    event = SomeEvent(uuid.uuid4(), version=2)

    event_store = MemoryEventStore()

    msg = f"expected version: 1, got {event.version}"
    with pytest.raises(ValueError, match=msg):
        event_store.append(event)


def test_load_event_stream():
    class SomeEvent(Event):
        pass

    id_ = uuid.uuid4()
    event1 = SomeEvent(id_, version=1)
    event2 = SomeEvent(id_, version=2)

    event_store = MemoryEventStore()
    event_store.append(event1)
    event_store.append(event2)

    assert list(event_store.load_event_stream(id_)) == [event1, event2]
