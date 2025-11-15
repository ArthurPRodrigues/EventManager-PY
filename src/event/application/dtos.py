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
    staffs_id: list[str] | None
    id: int | None = None


@dataclass(frozen=True)
class PaginatedEventsDto:
    event_list: list[Event]
    total_event_count: int


@dataclass(frozen=True)
class StaffDto:
    name: str
    email: str
    id: int | None = None


@dataclass(frozen=True)
class PaginatedStaffsDto:
    staff_list: list[StaffDto]
    total_staffs_count: int
