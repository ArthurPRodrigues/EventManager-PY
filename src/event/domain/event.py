from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime

from event.domain.errors import (
    InvalidCreatedAtError,
    InvalidEndDateError,
    InvalidLocationError,
    InvalidNameError,
    InvalidOrganizerIdError,
    InvalidStartDateError,
    InvalidTicketsAvailableError,
    StaffAlreadyAddedError,
)


@dataclass(frozen=True)
class Event:
    name: str
    location: str
    created_at: datetime
    start_date: datetime
    end_date: datetime
    tickets_available: int
    organizer_id: int
    staffs_id: list
    id: int | None = None

    @staticmethod
    def create(
        name: str,
        location: str,
        created_at: datetime,
        start_date: datetime,
        end_date: datetime,
        tickets_available: int,
        organizer_id: int,
    ) -> Event:
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
        if not tickets_available or not isinstance(tickets_available, int):
            raise InvalidTicketsAvailableError(tickets_available)
        if not organizer_id or not isinstance(organizer_id, int):
            raise InvalidOrganizerIdError(organizer_id)

        return Event(
            name=name,
            location=location,
            created_at=created_at,
            start_date=start_date,
            end_date=end_date,
            tickets_available=tickets_available,
            organizer_id=organizer_id,
        )

    def add_staff(self, staff_id: str) -> Event:
        if staff_id in self.staffs_id:
            raise StaffAlreadyAddedError(staff_id)
        return replace(self, staffs_id=[*self.staffs_id, staff_id])
