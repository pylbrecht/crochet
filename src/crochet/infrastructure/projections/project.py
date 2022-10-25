import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class Project:
    id: uuid.UUID
    name: str


class Projection(ABC):
    @abstractmethod
    def get_all(self) -> Iterable[Project]:
        pass

    @abstractmethod
    def get_by_id(self, id: uuid.UUID) -> Project:
        pass


class MemoryProjection(Projection):
    def __init__(self, projects: Optional[list[Project]] = None):
        projects = projects or []
        self._store = {project.id: project for project in projects}

    def get_all(self) -> Iterable[Project]:
        return self._store.values()

    def get_by_id(self, id: uuid.UUID) -> Project:
        try:
            return self._store[id]
        except KeyError:
            raise LookupError(f"project with id {id} not found")

    def save(self, project: Project):
        self._store[project.id] = project
