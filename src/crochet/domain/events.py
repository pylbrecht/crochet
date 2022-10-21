import uuid
from dataclasses import dataclass


@dataclass
class Event:
    stream_id: uuid.UUID
    version: int
