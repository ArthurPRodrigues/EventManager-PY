from __future__ import annotations

from dataclasses import dataclass

from events.application.errors import InvalidPageError, InvalidPageSizeError
from events.infra.persistence.sqlite_event_repository import SqliteEventRepository


@dataclass(frozen=True)
class ListEventInputDto:
    page: int = 1
    page_size: int = 10
    organizer_id: int | None = None


@dataclass(frozen=True)
class EventView:
    id: int
    name: str
    location: str
    start_date: str
    end_date: str
    tickets_available: int
    organizer_id: int
    created_at: str


@dataclass(frozen=True)
class ListEventsResult:
    items: list[EventView]
    total: int


class ListEventUseCase:
    def __init__(self, events_repository: SqliteEventRepository) -> None:
        self._events_repository = events_repository

    def execute(self, input_dto: ListEventInputDto) -> ListEventsResult:
        if input_dto.page < 1:
            raise InvalidPageError(input_dto.page)
        if input_dto.page_size < 1:
            raise InvalidPageSizeError(input_dto.page_size)

        rows, total = self._events_repository.list(
            page=input_dto.page,
            page_size=input_dto.page_size,
            organizer_id=input_dto.organizer_id,
        )

        views: list[EventView] = []
        for event in rows:
            (
                event_id,
                name,
                location,
                start_date,
                end_date,
                tickets_available,
                organizer_id,
                created_at,
            ) = event

            views.append(
                EventView(
                    id=event_id,
                    name=name,
                    location=location,
                    start_date=start_date,
                    end_date=end_date,
                    tickets_available=tickets_available,
                    organizer_id=organizer_id,
                    created_at=created_at,
                )
            )
        return ListEventsResult(items=views, total=total)
