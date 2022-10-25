import uuid

import pytest

from crochet.domain.events import NewProjectCreated
from crochet.infrastructure import projections
from crochet.interface.api import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_returns_created_project(client):
    payload = {"name": "test project"}
    response = client.post("/projects/", json=payload)

    assert response.status_code == 201
    assert response.json["id"]
    assert response.json["name"] == "test project"


def test_create_project(client):
    payload = {"name": "test project"}
    response = client.post("/projects/", json=payload)

    stream_id = uuid.UUID(response.json["id"])
    [event] = list(client.application.event_store.load_event_stream(stream_id))
    assert isinstance(event, NewProjectCreated)
    assert event.project_name == "test project"


def test_list_all_projects(client):
    project_id = uuid.uuid4()
    project = projections.project.Project(project_id, "a project")
    client.application.project_service.projection.save(project)

    response = client.get("/projects/")

    assert response.json == [
        {
            "id": str(project_id),
            "name": "a project",
        }
    ]
