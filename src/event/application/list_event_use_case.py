from __future__ import annotations

from dataclasses import dataclass

from event.application.dtos import PaginatedEventsDto
from event.infra.persistence.sqlite_event_repository import SqliteEventRepository


@dataclass(frozen=True)
class ListEventInputDto:
    page: int = 1
    page_size: int = 8
    filter_mode: str | None = None
    organizer_id: int | None = None
    user_id: int | None = None


class ListEventUseCase:
    def __init__(self, events_repository: SqliteEventRepository) -> PaginatedEventsDto:
        self._events_repository = events_repository

    def List_event(self, input_dto: ListEventInputDto) -> PaginatedEventsDto:
        paginated_events = self._events_repository.list(
            page=input_dto.page,
            page_size=input_dto.page_size,
            filter_mode=input_dto.filter_mode,
            organizer_id=input_dto.organizer_id,
            user_id=input_dto.user_id,
        )

        return paginated_events
