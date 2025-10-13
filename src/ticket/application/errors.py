from datetime import datetime

from user.domain.user_role import UserRole


class AppError(Exception):
    """Base class for tickets application errors."""


class UnauthorizedValidationError(AppError):
    def __init__(self, user_id: int, user_role: UserRole, code: str) -> None:
        message: str = f"User with ID '{user_id}' and role '{user_role.value}' is not authorized to validate ticket with code: {code}."
        super().__init__(message)


class TicketEventNotFoundError(AppError):
    def __init__(self, event_id: int) -> None:
        message: str = f"Event with ID '{event_id}' not found for ticket validation."
        super().__init__(message)


class TicketNotFoundError(AppError):
    def __init__(self, code: str) -> None:
        message: str = f"Ticket with code '{code}' not found."
        super().__init__(message)


class TicketValidationTimeError(AppError):
    def __init__(self, start_date: datetime, end_date: datetime, event_id: int) -> None:
        message: str = f"Cannot validate ticket for event with ID '{event_id}' because the event has either not started ({start_date}) or has already finished ({end_date})."
        super().__init__(message)
