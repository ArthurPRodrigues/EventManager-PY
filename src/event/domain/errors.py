from __future__ import annotations


class DomainError(Exception):
    """Base class for domain errors."""

class InvalidEventNameError(DomainError):
    def __init__(self, message: str = "Invalid event name.") -> None:
        super().__init__(message)

class InvalidTicketQuantityError(DomainError):
    def __init__(self, message: str = "Invalid ticket quantity, must be greater than 0.") -> None:
        super().__init__(message)

class InvalidEventDateError(DomainError):
    def __init__(self, message: str = "Invalid event date.") -> None:
        super().__init__(message)

class InvalidEventLocationError(DomainError):
    def __init__(self, message: str = "Invalid event location.") -> None:
        super().__init__(message)

class InvalidOrganizerIDError(DomainError):
    def __init__(self, message: str = "Invalid organizer email.") -> None:
        super().__init__(message)

