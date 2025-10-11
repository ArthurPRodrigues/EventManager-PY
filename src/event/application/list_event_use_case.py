from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from event.application.dtos import PaginatedEventsDto
from event.infra.persistence.sqlite_event_repository import SqliteEventRepository


@dataclass(frozen=True)
class ListEventInputDto:
    page: int = 1
    page_size: int = 10
    name: str | None = None
    location: str | None = None
    created_at: datetime | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    tickets_available: int | None = None
    organizer_id: int | None = None
    staffs_id: list[str] | None = None
    id: int | None = None
    filter_mode: str | None = None


class ListEventUseCase:
    def __init__(self, events_repository: SqliteEventRepository) -> PaginatedEventsDto:
        self._events_repository = events_repository

    def execute(self, input_dto: ListEventInputDto) -> PaginatedEventsDto:
        paginated_events = self._events_repository.list(
            page=input_dto.page,
            page_size=input_dto.page_size,
            name=input_dto.name,
            location=input_dto.location,
            created_at=input_dto.created_at,
            start_date=input_dto.start_date,
            end_date=input_dto.end_date,
            tickets_available=input_dto.tickets_available,
            organizer_id=input_dto.organizer_id,
            staffs_id=input_dto.staffs_id,
            id=input_dto.id,
            filter_mode=input_dto.filter_mode,
        )

        return paginated_events
