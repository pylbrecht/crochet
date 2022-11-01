from http import HTTPStatus

from flask import Blueprint, Flask
from flask import current_app as app
from flask import request
from flask_cors import CORS

from crochet.application.services import ProjectService
from crochet.domain.commands import CreateNewProject
from crochet.infrastructure import projections
from crochet.infrastructure.event_store import MemoryEventStore

bp = Blueprint("auth", __name__, url_prefix="/")


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)

    # FIXME: Enable CORS for all requests. This should only be done during
    # development.
    CORS(app)

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
    hook_size = request.json["hook_size"]

    cmd = CreateNewProject(name, hook_size)
    project = app.project_service.execute(cmd)

    response = {
        "id": project.id,
        "name": project.name,
        "hook_size": project.hook_size,
    }
    return response, HTTPStatus.CREATED


@bp.get("/projects/")
def get_projects():
    return [
        {
            "id": project.id,
            "name": project.name,
            "hook_size": project.hook_size,
        }
        for project in app.project_service.projection.get_all()
    ]
