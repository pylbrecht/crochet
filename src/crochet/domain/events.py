import uuid
from abc import ABC


class Event(ABC):
    def __init__(self, stream_id: uuid.UUID, version: int):
        self._stream_id = stream_id
        self._version = version

    @property
    def stream_id(self) -> uuid.UUID:
        return self._stream_id

    @property
    def version(self) -> int:
        return self._version

    @property
    def name(self) -> str:
        return self.__class__.__name__
