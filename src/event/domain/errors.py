from __future__ import annotations


class DomainError(Exception):
    """Base class for domain errors."""


class InvalidEventError(DomainError):
    def __init__(self, event) -> None:
        message = f'Invalid event: "{event}".'
        super().__init__(message)


class InvalidCreatedAtError(DomainError):
    def __init__(self, created_at) -> None:
        message = f'Invalid created_at: "{created_at}".'
        super().__init__(message)


class InvalidEndDateError(DomainError):
    def __init__(self, end_date) -> None:
        message = f'Invalid end_date: "{end_date}".'
        super().__init__(message)


class InvalidLocationError(DomainError):
    def __init__(self, location) -> None:
        message = f'Invalid location: "{location}".'
        super().__init__(message)


class InvalidNameError(DomainError):
    def __init__(self, name) -> None:
        message = f'Invalid name: "{name}".'
        super().__init__(message)


class InvalidStartDateError(DomainError):
    def __init__(self, start_date) -> None:
        message = f'Invalid start_date: "{start_date}".'
        super().__init__(message)


class InvalidMaxTicketsError(DomainError):
    def __init__(self, max_tickets) -> None:
        message = f'Invalid max_tickets: "{max_tickets}".'
        super().__init__(message)


class InvalidOrganizerIdError(DomainError):
    def __init__(self, organizer_id) -> None:
        message = f'Invalid organizer_id: "{organizer_id}".'
        super().__init__(message)


class InvalidStaffsIdError(DomainError):
    def __init__(self, staffs_id) -> None:
        message = f'Invalid staffs_id: "{staffs_id}".'
        super().__init__(message)


class StaffAlreadyAddedError(DomainError):
    def __init__(self, staff_id) -> None:
        message = f'Staff with id "{staff_id}" has already been added.'
        super().__init__(message)
