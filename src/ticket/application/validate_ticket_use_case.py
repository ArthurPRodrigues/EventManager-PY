from __future__ import annotations

from datetime import UTC, datetime

from event.domain.event import Event
from event.infra.persistence.sqlite_event_repository import SqliteEventRepository
from ticket.domain.ticket import Ticket
from ticket.infra.persistence.sqlite_tickets_repository import SqliteTicketsRepository
from user.domain.user_role import UserRole

from .dtos import ValidateTicketInputDto
from .errors import (
    TicketEventNotFoundError,
    TicketNotFoundError,
    TicketValidationTimeError,
    UnauthorizedValidationError,
)


class ValidateTicketUseCase:
    def __init__(
        self,
        tickets_repository: SqliteTicketsRepository,
        events_repository: SqliteEventRepository,
    ) -> None:
        self._tickets_repository = tickets_repository
        self._events_repository = events_repository

    def execute(self, input_dto: ValidateTicketInputDto) -> Ticket:
        user_id, user_role, code = (
            input_dto.user_id,
            input_dto.user_role,
            input_dto.code,
        )

        ticket: Ticket = self._tickets_repository.get_by_code(code)
        if ticket is None:
            raise TicketNotFoundError(code)

        event: Event = self._events_repository.get_by_id(ticket.event_id)
        if event is None:
            raise TicketEventNotFoundError(ticket.event_id)

        if datetime.now(UTC) < event.start_date or datetime.now(UTC) > event.end_date:
            raise TicketValidationTimeError(event.start_date, event.end_date, event.id)

        # Authorization check based on user role
        if user_role == UserRole.ORGANIZER:
            if event.organizer_id != user_id:
                raise UnauthorizedValidationError(user_id, user_role, code)
        elif user_role == UserRole.STAFF:
            if user_id not in event.staffs_id:
                raise UnauthorizedValidationError(user_id, user_role, code)

        validated_ticket = ticket.validate()
        self._tickets_repository.update(validated_ticket)
        return validated_ticket
