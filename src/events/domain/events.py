from dataclasses import dataclass
from datetime import date, datetime

from events.application.errors import PastDateError
from events.domain.errors import (
    InvalidCreatedAtError,
    InvalidEndDateError,
    InvalidLocationError,
    InvalidNameError,
    InvalidOrganizerIDError,
    InvalidStartDateError,
    InvalidTicketsAvailableError,
)


@dataclass(frozen=True)
class Events:
    created_at: datetime
    end_date: date
    location: str
    name: str
    start_date: date
    tickets_available: int
    organizer_id: int
    id: int | None = None

    @staticmethod
    def create(
        created_at: datetime,
        end_date: date,
        location: str,
        name: str,
        start_date: date,
        tickets_available: int,
        organizer_id: int,
    ) -> "Events":
        if not created_at or not isinstance(created_at, datetime):
            raise InvalidCreatedAtError(created_at)
        if not end_date or not isinstance(end_date, date):
            raise InvalidEndDateError(end_date)
        if not location or not isinstance(location, str):
            raise InvalidLocationError(location)
        if not name or not isinstance(name, str):
            raise InvalidNameError(name)
        if not start_date or not isinstance(start_date, date):
            raise InvalidStartDateError(start_date)
        if not tickets_available or not isinstance(tickets_available, int):
            raise InvalidTicketsAvailableError(tickets_available)
        if not organizer_id or not isinstance(organizer_id, int):
            raise InvalidOrganizerIDError(organizer_id)

        created_date = (
            created_at.date() if isinstance(created_at, datetime) else created_at
        )
        print(
            f"start_date: {type(start_date)} | end_date: {type(end_date)} | created_at: {type(created_at)}"
        )

        if start_date < created_date or end_date < created_date:
            raise PastDateError(start_date if start_date < created_date else end_date)

        return Events(
            created_at=created_at,
            end_date=end_date,
            location=location,
            name=name,
            start_date=start_date,
            tickets_available=tickets_available,
            organizer_id=organizer_id,
        )
