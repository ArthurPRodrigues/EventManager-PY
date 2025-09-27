from dataclasses import dataclass
from datetime import datetime

from events.domain.errors import (
    InvalidCreatedAtError,
    InvalidEndDateError,
    InvalidLocationError,
    InvalidNameError,
    InvalidOrganizerIDError,
    InvalidStartDateError,
    InvalidTicketsAvaliableError,
)


@dataclass(frozen=True)
class Events:
    created_at: datetime
    end_date: datetime
    id: int
    location: str
    name: str
    start_date: datetime
    tickets_available: int
    organizer_id: int

    @staticmethod
    def register(
        created_at: datetime,
        end_date: datetime,
        location: str,
        name: str,
        start_date: datetime,
        tickets_avaliable: int,
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
        if not tickets_avaliable or not isinstance(tickets_avaliable, int):
            raise InvalidTicketsAvaliableError(tickets_avaliable)
        if not organizer_id or not isinstance(organizer_id, int):
            raise InvalidOrganizerIDError(organizer_id)

        return Events(
            created_at=created_at,
            end_date=end_date,
            location=location,
            name=name,
            start_date=start_date,
            tickets_avaliable=tickets_avaliable,
            organizer_id=organizer_id,
        )
