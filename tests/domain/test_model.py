import uuid

import pytest

from crochet.domain.events import NewProjectCreated
from crochet.domain.model import Project


@pytest.mark.parametrize(
    "name",
    [
        "test project",
        "another test project",
    ],
)
def test_create_project_from_event(name):
    event = NewProjectCreated(stream_id=uuid.uuid4(), version=1, project_name=name)

    project = Project([event])

    assert project.name == name
