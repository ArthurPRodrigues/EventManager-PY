from __future__ import annotations

from dataclasses import dataclass

from event.application.errors import EventNotFoundError
from event.domain.event import Event
from event.infra.persistence.sqlite_event_repository import SqliteEventRepository


@dataclass(frozen=True)
class DeleteEventInputDto:
    event_id: int


class DeleteEventUseCase:
    def __init__(self, events_repository: SqliteEventRepository) -> None:
        self._events_repository = events_repository

    def execute(self, input_dto: DeleteEventInputDto) -> Event:
        event = self._events_repository.get_by_id(input_dto.event_id)
        if not event:
            raise EventNotFoundError(input_dto.event_id)

        self._events_repository.delete(event.id)
        return event
