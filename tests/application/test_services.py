import pytest

from crochet.application.services import ProjectService
from crochet.domain.commands import CreateNewProject
from crochet.infrastructure import projections
from crochet.infrastructure.event_store import MemoryEventStore


@pytest.mark.parametrize(
    "name",
    [
        "test project",
        "another test project",
    ],
)
def test_create_new_project(name):
    project_service = ProjectService(
        event_store=MemoryEventStore(),
        projection=projections.project.MemoryProjection(),
    )

    project = project_service.execute(CreateNewProject(project_name=name))

    assert project.name == name


def test_update_projection_upon_creation():
    project_service = ProjectService(
        event_store=MemoryEventStore(),
        projection=projections.project.MemoryProjection(),
    )

    name = "a project"
    project_service.execute(CreateNewProject(project_name=name))

    [project] = project_service.projection.get_all()
    assert project.id
    assert project.name == name
