from dataclasses import dataclass
from datetime import datetime

from event.domain.event import Event


@dataclass(frozen=True)
class EventDto:
    name: str
    location: str
    created_at: datetime
    start_date: datetime
    end_date: datetime
    max_tickets: int
    organizer_id: int
    id: int | None = None


@dataclass(frozen=True)
class PaginatedEventsDto:
    event_list: list[Event]
    total_event_count: int
