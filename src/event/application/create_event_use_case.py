from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from event.domain.errors import InvalidEventError
from event.domain.event import Event
from event.infra.persistence.sqlite_event_repository import SqliteEventRepository
from user.infra.persistence.sqlite_users_repository import SqliteUsersRepository


@dataclass(frozen=True)
class CreateEventInputDto:
    name: str
    start_date: date
    end_date: date
    location: str
    tickets_available: int
    organizer_id: int


class CreateEventUseCase:
    def __init__(
        self,
        events_repository: SqliteEventRepository,
        users_repository: SqliteUsersRepository,
    ) -> None:
        self._events_repository = events_repository
        self._users_repository = users_repository

    def execute(self, input_dto: CreateEventInputDto) -> Event:
        organizer_id = input_dto.organizer_id

        event = Event.create(
            name=input_dto.name,
            start_date=input_dto.start_date,
            end_date=input_dto.end_date,
            location=input_dto.location,
            tickets_available=input_dto.tickets_available,
            organizer_id=organizer_id,
            created_at=datetime.now(),
        )

        try:
            created_event = self._events_repository.add(event)
            return created_event

        except Exception as e:
            raise InvalidEventError(event) from e
