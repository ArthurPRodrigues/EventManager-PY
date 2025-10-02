from __future__ import annotations

from dataclasses import dataclass

from ticket.domain.ticket import Ticket
from ticket.infra.persistence.sqlite_tickets_repository import SqliteTicketsRepository
from user.domain.user_role import UserRole

from .errors import (
    TicketEventNotFoundError,
    TicketNotFoundError,
    UnauthorizedValidationError,
)


@dataclass(frozen=True)
class ValidateTicketInputDto:
    user_id: int
    user_role: UserRole
    code: str


class ValidateTicketUseCase:
    def __init__(
        self,
        tickets_repository: SqliteTicketsRepository,
        events_repository: SqliteEventRepository,  # noqa: F821
    ) -> None:
        self._tickets_repository = tickets_repository
        self._events_repository = events_repository

    def execute(self, input_dto: ValidateTicketInputDto) -> Ticket:
        user_id, user_role, normalized_code = (
            input_dto.user_id,
            input_dto.user_role,
            input_dto.code.strip().upper(),
        )

        if user_role == UserRole.CLIENT:
            raise UnauthorizedValidationError(user_id, user_role, normalized_code)

        ticket: Ticket = self._tickets_repository.get_by_code(normalized_code)
        if ticket is None:
            raise TicketNotFoundError(normalized_code)

        event = self._events_repository.get_by_id(ticket.event_id)
        if event is None:
            raise TicketEventNotFoundError(ticket.event_id)

        if user_role == UserRole.ORGANIZER:
            if event.organizer_id != user_id:
                raise UnauthorizedValidationError(user_id, user_role, normalized_code)

        if user_role == UserRole.STAFF:
            if user_id not in event.staff_ids:
                raise UnauthorizedValidationError(user_id, user_role, normalized_code)

        validated_ticket = ticket.validate()
        self._tickets_repository.update(validated_ticket)
        return validated_ticket
