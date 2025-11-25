from __future__ import annotations

from datetime import datetime


# TODO: Chante to AppError like event/application/errors.py and friendship/application/errors.py
# @ArthurPRodrigues
class AppError(Exception):
    """Base class for domain errors."""


# TODO: Remove unused errors
# @ArthurPRodrigues
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


class IncorrectEndDateError(AppError):
    def __init__(self) -> None:
        message = "The event's ending date is incorrect, it cannot be before the starting date."
        super().__init__(message)


class IncorrectTicketQuantityError(AppError):
    def __init__(self, max_tickets: int, tickets_redeemed: int) -> None:
        message = f"This event has {tickets_redeemed} tickets already redeemed, so the maximum tickets cannot be set to {max_tickets}."
        super().__init__(message)


class TicketsLowerThanAcceptedError(AppError):
    def __init__(self) -> None:
        message = "The number of tickets needs to be greater than zero."
        super().__init__(message)
