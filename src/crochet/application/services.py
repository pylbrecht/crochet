import uuid
from functools import singledispatchmethod
from typing import Any

from crochet.domain.commands import Command, CreateNewProject
from crochet.domain.events import NewProjectCreated
from crochet.domain.model import Project
from crochet.infrastructure import projections


class ProjectService:
    def __init__(
        self,
        event_store: Any,
        projection: projections.project.Projection,
    ):
        self.event_store = event_store
        self.projection = projection

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
            hook_size=command.hook_size,
        )
        self.event_store.append(event)
        self.projection.save(
            projections.project.Project(
                event.stream_id, event.project_name, event.hook_size
            )
        )
        return Project(self.event_store.load_event_stream(stream_id))
