import uuid

from crochet.domain.events import Event


def test_has_name_property():
    class SomeEvent(Event):
        pass

    event = SomeEvent(stream_id=uuid.uuid4(), version=1)
    assert event.name == "SomeEvent"


def test_has_id_property():
    class SomeEvent(Event):
        pass

    ident = uuid.uuid4()
    event = SomeEvent(stream_id=ident, version=1)
    assert event.stream_id == ident
