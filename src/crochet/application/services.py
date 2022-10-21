import uuid
from functools import singledispatchmethod
from typing import Any

from crochet.domain.commands import Command, CreateNewProject
from crochet.domain.events import NewProjectCreated
from crochet.domain.model import Project


class ProjectService:
    def __init__(self, event_store: Any):
        self.event_store = event_store

    def execute(self, command: Command) -> Any:
        return self.when(command)

    @singledispatchmethod
    def when(self, command: Command):
        raise NotImplementedError(f"cannot handle command {type(command)}")

    @when.register
    def _(self, command: CreateNewProject):
        # TODO: Implement some sort of identity provider to ensure uniqueness.
        stream_id = uuid.uuid4()
        event = NewProjectCreated(
            stream_id=stream_id,
            version=1,
            project_name=command.project_name,
        )
        self.event_store.append(event)
        return Project(self.event_store.load_event_stream(stream_id))
