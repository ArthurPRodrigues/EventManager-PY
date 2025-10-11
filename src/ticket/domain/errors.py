from __future__ import annotations


class DomainError(Exception):
    """Base class for domain errors."""


class InvalidEventIdError(DomainError):
    def __init__(self, event_id: int | str = "Invalid event id.") -> None:
        message: str = f"Invalid event ID: {event_id}"
        super().__init__(message)


class InvalidClientIdError(DomainError):
    def __init__(self, client_id: int | str = "Invalid client id.") -> None:
        message: str = f"Invalid client ID: {client_id}"
        super().__init__(message)


class InvalidTicketCodeError(DomainError):
    def __init__(self, ticket_code: str = "Invalid ticket code.") -> None:
        message: str = f"Invalid ticket code: {ticket_code}"
        super().__init__(message)


class TicketAlreadyValidatedError(DomainError):
    def __init__(self, message: str = "Ticket has already been validated.") -> None:
        super().__init__(message)
