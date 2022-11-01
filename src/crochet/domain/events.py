import uuid
from dataclasses import dataclass


@dataclass
class Event:
    stream_id: uuid.UUID
    version: int


@dataclass
class NewProjectCreated(Event):
    project_name: str
    hook_size: str
