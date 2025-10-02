from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from user.infra.persistence.sqlite_users_repository import SqliteUsersRepository

from events.domain.events import Events
from events.infra.persistence.SqliteEventsRepository import SqliteEventsRepository

@dataclass(frozen=True)
class CreateEventInputDto:
    name: str
    start_date: datetime
    end_date: datetime
    location: str
    tickets_available: int
    organizer_id: int

class CreateEventUseCase:
    def __init__(self, events_repository: SqliteEventsRepository, users_repository: SqliteUsersRepository) -> None:
        self._events_repository = events_repository
        self._users_repository = users_repository

    def execute(self, input_dto: CreateEventInputDto) -> Events:
        organizer_id = input_dto.organizer_id

        event = Events.register(
            name = input_dto.name,
            start_date = input_dto.start_date,
            end_date = input_dto.end_date,
            location = input_dto.location,
            tickets_available = input_dto.tickets_available,
            organizer_id = organizer_id,
            created_at= datetime.now()
        )

        created_event = self._events_repository.add(event)
        return created_event