from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from event.domain.event import Event
from event.infra.persistence.sqlite_event_repository import SqliteEventRepository


@dataclass(frozen=True)
class CreateEventInputDto:
    name: str
    start_date: datetime
    end_date: datetime
    location: str
    max_tickets: int
    organizer_id: int


class CreateEventUseCase:
    def __init__(self, events_repository: SqliteEventRepository) -> None:
        self._events_repository = events_repository

    def create_event(self, input_dto: CreateEventInputDto) -> Event:
        event = Event.create(
            name=input_dto.name,
            start_date=input_dto.start_date,
            end_date=input_dto.end_date,
            location=input_dto.location,
            max_tickets=input_dto.max_tickets,
            organizer_id=input_dto.organizer_id,
            created_at=datetime.now(UTC),
        )

        created_event = self._events_repository.add(event)
        return created_event
