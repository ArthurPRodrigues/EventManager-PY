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
        ticket = self._get_ticket_or_raise(input_dto.code)
        event = self._get_event_or_raise(ticket.event_id)

        self._validate_event_time(event)
        self._validate_authorization(
            input_dto.user_id, input_dto.user_role, event, input_dto.code
        )

        validated_ticket = ticket.validate()
        self._tickets_repository.update(validated_ticket)
        return validated_ticket

    def _get_ticket_or_raise(self, code: str) -> Ticket:
        ticket = self._tickets_repository.get_by_code(code)
        if ticket is None:
            raise TicketNotFoundError(code)
        return ticket

    def _get_event_or_raise(self, event_id: int) -> Event:
        event = self._events_repository.get_by_id(event_id)
        if event is None:
            raise TicketEventNotFoundError(event_id)
        return event

    def _validate_event_time(self, event: Event) -> None:
        now = datetime.now(UTC)
        if not (event.start_date <= now <= event.end_date):
            raise TicketValidationTimeError(event.start_date, event.end_date, event.id)

    def _validate_authorization(
        self, user_id: int, user_role: UserRole, event: Event, code: str
    ) -> None:
        if user_role == UserRole.ORGANIZER:
            if event.organizer_id != user_id:
                raise UnauthorizedValidationError(user_id, user_role, code)
        elif user_role == UserRole.STAFF:
            if user_id not in event.staffs_id:
                raise UnauthorizedValidationError(user_id, user_role, code)
