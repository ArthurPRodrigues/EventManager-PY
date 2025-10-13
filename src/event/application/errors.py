from __future__ import annotations

from datetime import datetime


class AppError(Exception):
    """Base class for application errors."""


class InvalidPageSizeError(AppError):
    def __init__(self, size: int) -> None:
        message = f"Invalid page size: {size}."
        super().__init__(message)


class InvalidPageError(AppError):
    def __init__(self, page: int) -> None:
        message = f"Invalid page number: {page}."
        super().__init__(message)


class PastDateError(AppError):
    def __init__(self, date: datetime) -> None:
        message = f"The date {date} is incorrect, it cannot be in the past."
        super().__init__(message)


class EventNotFoundError(AppError):
    def __init__(self, event_id: int) -> None:
        message = f"Event with ID {event_id} not found."
        super().__init__(message)


class IncorrectOrganizerError(AppError):
    def __init__(self, organizer_name: str, event_name: str) -> None:
        message = f"User {organizer_name} is not the organizer of event {event_name}."
        super().__init__(message)


class IncorrectEndDateError(AppError):
    def __init__(self) -> None:
        message = "The event's ending date is incorrect, it cannot be before the starting date."
        super().__init__(message)
