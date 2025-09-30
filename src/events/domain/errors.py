from __future__ import annotations


class DomainError(Exception):
    """Base class for domain errors."""


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


class InvalidTicketsAvailableError(DomainError):
    def __init__(self, tickets_available) -> None:
        message = f'Invalid tickets_available: "{tickets_available}".'
        super().__init__(message)


class InvalidPageSizeError(DomainError):
    def __init__(self, size: int) -> None:
        message = f"Invalid page size: {size}."
        super().__init__(message)


class InvalidPageError(DomainError):
    def __init__(self, page: int) -> None:
        message = f"Invalid page number: {page}."
        super().__init__(message)


class InvalidOrganizerIDError(DomainError):
    def __init__(self, organizer_id) -> None:
        message = f'Invalid organizer_id: "{organizer_id}".'
        super().__init__(message)
