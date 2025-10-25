from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from event.domain.errors import InvalidOrganizerIdError
from event.domain.event import Event
from event.infra.persistence.sqlite_event_repository import SqliteEventRepository
from user.infra.persistence.sqlite_users_repository import SqliteUsersRepository


@dataclass(frozen=True)
class CreateEventInputDto:
    name: str
    start_date: datetime
    end_date: datetime
    location: str
    max_tickets: int
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
        if not organizer_id or not self._users_repository.get_by_id(organizer_id):
            raise InvalidOrganizerIdError(organizer_id)

        event = Event.create(
            name=input_dto.name,
            start_date=input_dto.start_date,
            end_date=input_dto.end_date,
            location=input_dto.location,
            max_tickets=input_dto.max_tickets,
            organizer_id=organizer_id,
            created_at=datetime.now(),
        )

        created_event = self._events_repository.add(event)
        return created_event
