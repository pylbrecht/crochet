from http import HTTPStatus

from flask import Blueprint, Flask
from flask import current_app as app
from flask import request

from crochet.application.services import ProjectService
from crochet.domain.commands import CreateNewProject
from crochet.infrastructure import projections
from crochet.infrastructure.event_store import MemoryEventStore

bp = Blueprint("auth", __name__, url_prefix="/")


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)

    # TODO: replace this with a proper dependency container
    app.event_store = MemoryEventStore()
    app.project_service = ProjectService(
        app.event_store, projections.project.MemoryProjection()
    )

    return app


@bp.post("/projects/")
def create_project():
    # TODO: add payload validation
    name = request.json["name"]

    cmd = CreateNewProject(name)
    project = app.project_service.execute(cmd)

    response = {
        "id": project.id,
        "name": project.name,
    }
    return response, HTTPStatus.CREATED
