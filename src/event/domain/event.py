from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime

from event.application.errors import IncorrectEndDateError, PastDateError
from event.domain.errors import (
    InvalidCreatedAtError,
    InvalidEndDateError,
    InvalidLocationError,
    InvalidMaxTicketsError,
    InvalidNameError,
    InvalidOrganizerIdError,
    InvalidStartDateError,
    StaffAlreadyAddedError,
)


@dataclass(frozen=True)
class Event:
    name: str
    location: str
    created_at: datetime
    start_date: datetime
    end_date: datetime
    organizer_id: int
    max_tickets: int
    initial_max_tickets: int = 0
    tickets_redeemed: int = 0
    staffs_id: list[str] = None
    id: int | None = None

    @staticmethod
    def create(
        name: str,
        location: str,
        created_at: datetime,
        start_date: datetime,
        end_date: datetime,
        max_tickets: int,
        organizer_id: int,
    ) -> Event:
        if Event.all_validations(
            name, location, created_at, start_date, end_date, organizer_id, max_tickets
        ):
            return Event(
                name=name,
                location=location,
                created_at=created_at,
                start_date=start_date,
                end_date=end_date,
                max_tickets=max_tickets,
                initial_max_tickets=max_tickets,
                organizer_id=organizer_id,
            )

    def add_staff(self, staff_id: str) -> Event:
        if staff_id in self.staffs_id:
            raise StaffAlreadyAddedError(staff_id)
        return replace(self, staffs_id=[*self.staffs_id, staff_id])

    @staticmethod
    def all_validations(
        name,
        location,
        created_at,
        start_date,
        end_date,
        organizer_id,
        max_tickets,
    ):
        if not name or not isinstance(name, str) or not name.strip():
            raise InvalidNameError(name)
        if not location or not isinstance(location, str) or not location.strip():
            raise InvalidLocationError(location)
        if not created_at or not isinstance(created_at, datetime):
            raise InvalidCreatedAtError(created_at)
        if not start_date or not isinstance(start_date, datetime):
            raise InvalidStartDateError(start_date)
        if not end_date or not isinstance(end_date, datetime):
            raise InvalidEndDateError(end_date)
        if not organizer_id or not isinstance(organizer_id, int):
            raise InvalidOrganizerIdError(organizer_id)

        if start_date < created_at or end_date < created_at:
            raise PastDateError(start_date if start_date < created_at else end_date)

        if end_date < start_date:
            raise IncorrectEndDateError()

        if not isinstance(max_tickets, int) or max_tickets < 0:
            raise InvalidMaxTicketsError(max_tickets)

        return True
