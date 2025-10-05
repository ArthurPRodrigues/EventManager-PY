class DomainError(Exception):
    """Base class for domain errors."""


class InvalidCodeError(DomainError):
    def __init__(self, ticket_code) -> None:
        message = f'Invalid code: "{ticket_code}".'
        super().__init__(message)


class InvalidStatusError(DomainError):
    def __init__(self, ticket_status) -> None:
        message = f'Invalid status: "{ticket_status}".'
        super().__init__(message)


class InvalidEventIdError(DomainError):
    def __init__(self, event_id) -> None:
        message = f'Invalid event ID: "{event_id}".'
        super().__init__(message)


class InvalidClientIdError(DomainError):
    def __init__(self, client_id) -> None:
        message = f'Invalid client ID: "{client_id}".'
        super().__init__(message)


class TicketNotFoundError(DomainError):
    def __init__(self, ticket_id) -> None:
        message = f'Ticket with ID "{ticket_id}" not found.'
        super().__init__(message)


class TicketAlreadyUsedError(DomainError):
    def __init__(self, ticket_id) -> None:
        message = f'Ticket with ID "{ticket_id}" has already been used.'
        super().__init__(message)


class TicketNotActiveError(DomainError):
    def __init__(self, ticket_id) -> None:
        message = f'Ticket with ID "{ticket_id}" is not active.'
        super().__init__(message)


class TicketAlreadyUsedError(DomainError):
    def __init__(self, ticket_id) -> None:
        message = f'Ticket with ID "{ticket_id}" has already been used.'
        super().__init__(message)


class TicketNotActiveError(DomainError):
    def __init__(self, ticket_id) -> None:
        message = f'Ticket with ID "{ticket_id}" is not active.'
        super().__init__(message)
