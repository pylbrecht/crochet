import uuid
from dataclasses import dataclass


@dataclass
class Command:
    stream_id: uuid.UUID
    version: int


@dataclass
class CreateNewProject(Command):
    project_name: str
