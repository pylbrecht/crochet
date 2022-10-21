from dataclasses import dataclass


class Command:
    pass


@dataclass
class CreateNewProject(Command):
    project_name: str
