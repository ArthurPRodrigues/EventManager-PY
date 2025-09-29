from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .errors import (
    InvalidTicketQuantityError,
    InvalidEventNameError,
    InvalidEventDateError,
    InvalidEventLocationError,
    InvalidOrganizerIDError
)


@dataclass(frozen=True)
class Event: 
    id: int | None = None
    name: str
    location: str
    start_date: datetime
    end_date: datetime
    created_at: datetime
    tickets_available: int
    organizer_id: int

    @staticmethod
    def create(
        name: str,
        start_date: datetime,
        end_date: datetime,
        location: str,
        tickets_available: int,
        organizer_id: int,
    ) -> "Event":
        if not name or not name.strip():
            raise InvalidEventNameError()
        if not isinstance(start_date, datetime):
            raise InvalidEventDateError()
        if not isinstance(end_date, datetime):
            raise InvalidEventDateError()
        if not location or not location.strip():
            raise InvalidEventLocationError()
        if not isinstance(tickets_available, int) or tickets_available < 0:
            raise InvalidTicketQuantityError()
        if not organizer_id:
            raise InvalidOrganizerIDError()
        
        return Event(
            name = name.strip(),
            start_date = start_date,
            end_date = end_date,
            location = location,
            tickets_available = tickets_available,
            organizer_id = organizer_id,
        )
    
    def has_tickets(self) -> bool:
        return self.tickets_available > 0
