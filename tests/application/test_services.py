import pytest

from crochet.application.services import ProjectService
from crochet.domain.commands import CreateNewProject
from crochet.infrastructure import projections
from crochet.infrastructure.event_store import MemoryEventStore


@pytest.mark.parametrize(
    "name,hook_size",
    [
        ("test project", "42"),
        ("another test project", "42"),
    ],
)
def test_create_new_project(name, hook_size):
    project_service = ProjectService(
        event_store=MemoryEventStore(),
        projection=projections.project.MemoryProjection(),
    )

    project = project_service.execute(
        CreateNewProject(project_name=name, hook_size=hook_size)
    )

    assert project.name == name


def test_update_projection_upon_creation():
    project_service = ProjectService(
        event_store=MemoryEventStore(),
        projection=projections.project.MemoryProjection(),
    )

    name = "a project"
    hook_size = "42"
    cmd = CreateNewProject(project_name=name, hook_size=hook_size)
    project_service.execute(cmd)

    [project] = project_service.projection.get_all()
    assert project.id
    assert project.name == name
