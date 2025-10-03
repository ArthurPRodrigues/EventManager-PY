from dataclasses import dataclass
from datetime import datetime

from events.domain.errors import (
    InvalidCreatedAtError,
    InvalidEndDateError,
    InvalidLocationError,
    InvalidNameError,
    InvalidOrganizerIDError,
    InvalidStartDateError,
    InvalidTicketsAvailableError,
)

from events.application.errors import PastDateError


@dataclass(frozen=True)
class Events:
    created_at: datetime
    end_date: datetime
    location: str
    name: str
    start_date: datetime
    tickets_available: int
    organizer_id: int
    id: int | None = None

    @staticmethod
    def create(
        created_at: datetime,
        end_date: datetime,
        location: str,
        name: str,
        start_date: datetime,
        tickets_available: int,
        organizer_id: int,
    ) -> "Events":
        if not created_at or not isinstance(created_at, datetime):
            raise InvalidCreatedAtError(created_at)
        if not end_date or not isinstance(end_date, datetime):
            raise InvalidEndDateError(end_date)
        if not location or not isinstance(location, str):
            raise InvalidLocationError(location)
        if not name or not isinstance(name, str):
            raise InvalidNameError(name)
        if not start_date or not isinstance(start_date, datetime):
            raise InvalidStartDateError(start_date)
        if not tickets_available or not isinstance(tickets_available, int):
            raise InvalidTicketsAvailableError(tickets_available)
        if not organizer_id or not isinstance(organizer_id, int):
            raise InvalidOrganizerIDError(organizer_id)
        
        if start_date < created_at or end_date < created_at:
            raise PastDateError(start_date if start_date < created_at else end_date)

        return Events(
            created_at=created_at,
            end_date=end_date,
            location=location,
            name=name,
            start_date=start_date,
            tickets_available=tickets_available,
            organizer_id=organizer_id,
        )
