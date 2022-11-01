import uuid
from functools import singledispatchmethod

from .events import Event, NewProjectCreated


class Project:
    """A crochet project"""

    def __init__(self, events: list[Event]):
        for event in events:
            self.when(event)

    @singledispatchmethod
    def when(self, event: Event):
        raise NotImplementedError(f"cannot apply event {type(event)}")

    @when.register
    def _(self, event: NewProjectCreated):
        self._name = event.project_name
        self._id = event.stream_id
        self._hook_size = event.hook_size

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def hook_size(self) -> str:
        return self._hook_size
